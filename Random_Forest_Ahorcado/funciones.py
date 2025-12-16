import requests, time
import pandas as pd
import random
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
import joblib
import sqlite3
import matplotlib.pyplot as plt

def f_conexion_bd(url_bd, nombre_log):  #Establece la conexión una base de datos. Devuelve la conexión.

    # Limpiamos el nombre del archivo
    nombre_archivo = url_bd.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(nombre_archivo)
        print(f"📁 Base de datos SQLite {nombre_log} conectada.")
        return conn
    except Exception as e:
        raise RuntimeError(f"Error SQLite: {e}")

#-------------------------------------------
#-------------------------------------------
#-------------------------------------------

def f_llamada_api(api_url, api_nombre): #Establece la conexión a una API. Devuelve el json de respuesta.
    for i in range(10):
        try:
            
            response = requests.get(api_url)
            # print(f"API {api_nombre} conectada con éxito")
            return response
        
        except requests.exceptions.RequestException as e:
            print(f"Intento {i+1}: la API {api_nombre} aún no está lista. Esperando...")
            time.sleep(2)
    raise RuntimeError(f"No se pudo conectar a la API {api_nombre} tras 10 intentos")

#-------------------------------------------
#-------------------------------------------
#-------------------------------------------

def f_generar_bloque_datos(lista_palabras, simulaciones_por_palabra, abecedario):   #Se la llama desde la función f_ejecutar_etl. Devuelve el dataframe completo de las simulaciones.

    # print(f"* Simulando {len(lista_palabras)} palabras *")
    datos_entrada = []
    datos_salida = []
    
    for palabra in lista_palabras:

        # Validamos que todas las letras de la palabra están en nuestro abecedario. Sino salta la palabra
        if not all(c in abecedario for c in palabra):
            continue
            
        longitud = len(palabra)
        unicas = len(set(palabra))
        
        # Target: es un vector con 1 para la letras de nuestro abecedario contenidas en la palabra y 0 las que no
        target_vector = [1 if letra in palabra else 0 for letra in abecedario]
        
        for _ in range(simulaciones_por_palabra):

            # Simulación aleatoria de partidas. Elejirá cuantas letras se han probado ya y cuales.
            n_letras_probadas = random.randint(0, len(abecedario))              # De forma aleatoria elije el número de letras que se han probado. Devuelve un entero
            letras_probadas = random.sample(abecedario, n_letras_probadas)      # En base al número de letras probadas, devuelve una lista aleatoria de las letras.
            
            # Aquí se generan las features. Comprueba si la letra no se ha probado (0), se ha probado y se ha acertado (1) o no se ha acertado (-1)
            estado_letras = []
            for letra in abecedario:
                if letra not in letras_probadas:
                    estado_letras.append(0) # No probada
                elif letra in palabra:
                    estado_letras.append(1) # Acierto
                else:
                    estado_letras.append(-1) # Fallo
            
            datos_entrada.append([longitud, unicas] + estado_letras)    # Se incluye a la lista de features los valores estáticos de la palabra (Longitud y letras únicas)
            datos_salida.append(target_vector)

    # Se generan los nombres de las columnas. Como tenemos que 32 letras en el abecedario, necesitamos 32 columnas del estado de las letras (0)(1)(-1) + 2 columnas estáticas
    # Las columnas del target serán 32 con valores (0)(1) si está contenida realmente la letra en la palabra.
    
    col_features = ['longitud', 'unicas'] + [f'estado_{l}' for l in abecedario] # 34 columnas features
    col_target = [f'es_{l}' for l in abecedario] # 32 columnas features
    
    # Generamos las columnas del DataFrame
    df_X = pd.DataFrame(datos_entrada, columns=col_features)
    df_y = pd.DataFrame(datos_salida, columns=col_target)
    
    # Unimos las columnas de features y targets en un solo gran DataFrame
    df_completo = pd.concat([df_X, df_y], axis=1)
    
    return df_completo

#-------------------------------------------
#-------------------------------------------
#-------------------------------------------

def f_ejecutar_etl(lista_palabras_total, url_db, nombre_tabla, abecedario, simulaciones=50, tamano_lote=5000):  #Genera las partidas simuladas con la función f_generar_bloque_datos y las carga en la BD. No devuelve nada.


    
    
    # Usamos SQLAlchemy solo para crear la estructura de la tabla al principio, así poder usar la función .to_sql de Pandas
    t0 = time.time()
    engine = create_engine(url_db) # Para la conexión a la BD con grandes volúmenes, pandas no trabaja bien con objetos psycopg.Connection. Por eso se utiliza create_engine de la librería sqlalchemy
    
    total_palabras = len(lista_palabras_total)

    print(f"\n--- Cargando {total_palabras} palabras ---\n")
    print(f"🚀 Iniciando ETL con SQLite en: {url_db}")
    # -----------------------------------
    
    print("1. Creando estructura de tabla...")

    # Generamos 1 fila de prueba para utilizar las columnas para generar la tabla vacía. El df_dummy se generará con 1 palabra y 1 simulación
    df_dummy = f_generar_bloque_datos(lista_palabras_total[:1], 1, abecedario)
    df_dummy.head(0).to_sql(nombre_tabla, engine, if_exists='replace', index=False)     # Crea la tabla vacía en la bd, sólo las columnas
    
    
    total_palabras = len(lista_palabras_total)
    print(f"2. Iniciando carga de {total_palabras}...")

    palabras_cargadas = 0

    # Generamos los lotes de subida. El bucle iterará entre la lista total en golpes del tamaño de lote siendo 0 el inicial
    for i in range(0, total_palabras, tamano_lote):
        fin = min(i + tamano_lote, total_palabras)
        lote = lista_palabras_total[i : fin]        #Se genera el sublote
        palabras_cargadas += len(lote)
        
        # print(f"   > Procesando {i} a {fin} palabras...")
        df_lote = f_generar_bloque_datos(lote, simulaciones, abecedario)
        
        if not df_lote.empty:
            # Cargamos parte de df con la función .to_sql nativa de Pandas. Antes con la bd postgres teníamos que hacer un COPY en la función f_carga_postgres
            df_lote.to_sql(nombre_tabla, engine, if_exists='append', index=False)
            # print(f"     -> {len(df_lote)} filas insertadas.")
            print(f"Cargadas {round((palabras_cargadas*100)/total_palabras)}%")
            
            
        del df_lote # Nos aseguramos que python borre la memoria ram en cada iteración
    
    # Sacamos el total de registros guardados
    try:
        
        # Abrimos la conexión
        conn_conteo = f_conexion_bd(url_db, "Conteo Final")
        cur_conteo = conn_conteo.cursor()
        
        # Ejecutamos la query para contar
        cur_conteo.execute(f"SELECT COUNT(*) FROM {nombre_tabla};") 
        
        # Obtenemos el resultado (fetchone devuelve una tupla, ej: (5000000,))
        total_real = cur_conteo.fetchone()[0]
        
        print(f"✅ Datos correctamente cargados: {total_real:,} registros en {int((time.time() - t0) // 60)} minutos y {int((time.time() - t0) % 60)} segundos.!")
        
        cur_conteo.close()
        conn_conteo.close()
        
    except Exception as e:
        print(f"⚠️ Hubo un error al intentar contar los registros: {e}")

    print("\n--- Fin carga ---\n")

#-------------------------------------------
#-------------------------------------------
#-------------------------------------------

def f_entrenar_modelo(url_db, nombre_tabla, abecedario):    #Entrena el modelo Random Forest por lotes con el parámetro warm_start. Devuelve el modelo

    print("--- Entrenamiento modelo ---\n")
    print("🚀 Iniciando entrenamiento INCREMENTAL (Warm Start)...")
    
    BATCH_SIZE = 50000        # Procesamos 50.000 filas cada vez
    ARBOLES_POR_LOTE = 10     # Añadimos 10 árboles en cada vuelta
    MAX_ARBOLES = 200         # Queremos un bosque final de máximo 200 árboles
    
    t0 = time.time()
    
    # Definimos el modelo vacío. Con warm_start=True establecemos que en cada iteración "no olvide" los árboles ya aprendidos
    clf = RandomForestClassifier(
        n_estimators=0,       # Empezamos con 0 árboles
        warm_start=True,      # Mantiene lo aprendido en la siguiente llamada a .fit()
        n_jobs=-1,            # Usa todos los núcleos para entrenar el modelo, lo que generará "una copia" del df de ese chunk en cada núcleo
        random_state=42,
    )
    
    # Conexión y Lectura por Trozos (Chunks)
    # Usamos SQLAlchemy
    engine = create_engine(url_db)
    
    # Pandas read_sql con 'chunksize' devuelve un iterador, no carga todo de golpe. Big Data/Streaming
    # Es importante que sea aleatorio, porque de lo contrario los primero 10 árboles se entrenaría sólo con palabras que empiezan por a y caeríamos en el sesgo
    print("  Conectando y leyendo datos en streams...")
    chunks = pd.read_sql(
        f"SELECT * FROM {nombre_tabla} ORDER BY RANDOM()", 
        engine, 
        chunksize=BATCH_SIZE
    )
    
    # Columnas del dataframe
    cols_features = ['longitud', 'unicas'] + [f'estado_{l}' for l in abecedario]
    cols_target = [f'es_{l}' for l in abecedario]
    
    lote_num = 0
    
    # Bucle de Entrenamiento por chunks. Así no saturamos la memoria con un súper dataframe que se copiará 1 vez por nucleo
    for df_chunk in chunks:

        lote_num += 1
        # print(f"📦 Procesando Lote {lote_num} ({len(df_chunk)} filas)")
        
        # Optimizamos el tipo de datos almacenado para reducir el almacenamiento en un 70% aprox. Por defecto, Docker tiene un límite de 2Gb de uso de tu ram.
        # Si la columna es numérica, la bajamos al tipo más pequeño posible (int8/int16) porque se carga por defecto como int64
        for col in df_chunk.columns:
            if pd.api.types.is_numeric_dtype(df_chunk[col]):
                df_chunk[col] = pd.to_numeric(df_chunk[col], downcast='integer')
        
        # Separar X e y
        X_batch = df_chunk[cols_features]
        y_batch = df_chunk[cols_target]
        
        # Aumentamos en ARBOLES_POR_LOTE el número de árboles. Si entrenamos con 0 árboles dará error
        clf.n_estimators += ARBOLES_POR_LOTE
        
        # Entrenamos sólo con el df del chunk (pero añade los árboles al bosque global por el parámetro warn_start, no olvida los árboles anteriores)
        clf.fit(X_batch, y_batch)
        
        # print(f"     Bosque crecido a {clf.n_estimators} árboles. RAM liberada.")
        
        # Si llegamos al máximo de árboles corta el bucle
        if clf.n_estimators >= MAX_ARBOLES:
            print("🛑 Se alcanzó el número máximo de árboles.")
            break
            
        # Limpiamos las variables del bucle
        del df_chunk, X_batch, y_batch

    print(f"  TOTAL de álboles: {clf.n_estimators}")

    # Guardamos el modelo

    archivo_modelo = 'modelo_ahorcado.pkl'
    # print(f"💾 Guardando modelo en '{archivo_modelo}'...")
    joblib.dump(clf, archivo_modelo)
    print(f"✅ ¡Modelo guardado y listo para probar en {int((time.time() - t0) // 60)} minutos y {int((time.time() - t0) % 60)} segundos.!")
    print("\n--- Fin entrenamiento ---\n")
    return(clf)

#-------------------------------------------
#-------------------------------------------
#-------------------------------------------

def f_predecir_palabra(modelo, palabra, abecedario,contador_palabras):  #Prueba el algoritmo con la palabra dada. Devuelve el número de intentos para acertarla.

    # Validamos que todas las letras de la palabra están en nuestro abecedario. Sino salta la palabra
    for letra in palabra:
        if letra not in abecedario:
            print(f"La palabra {palabra} contiene la letra {letra} que no está contenida en nuestro abecedario")
            return 0

    t0 = time.time()

    datos_entrada = []

    longitud = len(palabra)
    unicas = len(set(palabra))

    estado_letras = []

    for letra in abecedario:
        estado_letras.append(0) # No probada

    datos_entrada.append([longitud, unicas] + estado_letras)    # Se incluye a la lista de features los valores estáticos de la palabra (Longitud y letras únicas)

    # Se generan los nombres de las columnas. Como tenemos que 32 letras en el abecedario, necesitamos 32 columnas del estado de las letras (0)(1)(-1) + 2 columnas estáticas
    # Las columnas del target serán 32 con valores (0)(1) si está contenida realmente la letra en la palabra.
    
    col_features = ['longitud', 'unicas'] + [f'estado_{l}' for l in abecedario] # 34 columnas features
    
    # Generamos las columnas del DataFrame
    df_X = pd.DataFrame(datos_entrada, columns=col_features)

    # predict_proba devuelve una lista de arrays (uno por cada letra del abecedario)
    all_probs = modelo.predict_proba(df_X)
    
    # Transferimos las probabilidades por letra a una lista
    lista_probs = []
    for proba_array in all_probs:
        lista_probs.append(proba_array.tolist())

    # print(f"Lista de probabilidades: {lista_probs}")

    #separamos del array sólo las probabilidades de la clase 1, es decir de que la letra esté en la palabra
    # p.shape[1] se refiere al tamaño, es decir hay veces que el array es así array([[1.0]]) y solo tiene columna 0 para letras raras. Entonces pone 0.0
    probs_clase_1 = [p[0][1] if p.shape[1] == 2 else 0.0 for p in all_probs]

    # Encontramos la letra ganadora por el índice de la máxima probabilidad
    indice_maximo = probs_clase_1.index(max(probs_clase_1))
    letra_ganadora = abecedario[indice_maximo]

    # print(f"🏆 Letra ganadora: {letra_ganadora} ({probabilidad:.2%})")


    contador_intentos = 0
    letras_acertadas = []
    letras_falladas = []

    # En este bucle se prueba la letra ganadora y en función del resultado recalcula la probabilidad.
    while True:

        if len(letras_acertadas) == unicas:
            print(f"Palabra {contador_palabras+1}: \"{palabra}\" acertada en {contador_intentos} intentos ({time.time() - t0:.2f} s). Letras acertadas {letras_acertadas}. Letras falladas {letras_falladas}")
            break

        elif letra_ganadora in palabra:
            estado_letras[indice_maximo] = 1
            letras_acertadas.append(letra_ganadora)
            contador_intentos += 1
        
        else:
            estado_letras[indice_maximo] = -1
            letras_falladas.append(letra_ganadora)
            contador_intentos += 1

        datos_entrada = []
        datos_entrada.append([longitud, unicas] + estado_letras)
        df_X = pd.DataFrame(datos_entrada, columns=col_features)
        all_probs = modelo.predict_proba(df_X)
        probs_clase_1 = [p[0][1] if p.shape[1] == 2 else 0.0 for p in all_probs]

        # Ponemos a -1 la probabilidad de cualquier letra que ya hayamos usado
        # para que 'max()' nunca la elija.
        # enumerate devuelve parejas de (posición, valor) de la lista abecedario
        for i, letra in enumerate(abecedario):
            if letra in letras_acertadas or letra in letras_falladas:
                probs_clase_1[i] = -1.0

        indice_maximo = probs_clase_1.index(max(probs_clase_1))
        letra_ganadora = abecedario[indice_maximo]
    
    return contador_intentos

#-------------------------------------------
#-------------------------------------------
#-------------------------------------------

def f_fuerza_bruta(palabra):    #Resuelve la palabra por fuerza bruta probando cada letra el abecedario. Devuelve el número de intentos para acertarla.

    abecedario = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g',
    'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'ñ', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z',
    'á', 'é', 'í', 'ó', 'ú', "ü"
    ]
    unicas = len(set(palabra))
    contador_acertadas = 0
    intentos = 0

    for letra in abecedario:

        if contador_acertadas == unicas:
            break

        elif letra in palabra:
            contador_acertadas += 1
            intentos += 1
        
        else:
            intentos += 1

    return intentos

#-------------------------------------------
#-------------------------------------------
#-------------------------------------------

def f_guardar_resultados(url_db,lista_columnas,lista_resultados,nombre_tabla):  #Guarda los resultados en la tabla nombre_tabla de la BD. No devuelve nada.

    engine = create_engine(url_db)

    df_result = pd.DataFrame(lista_resultados, columns=lista_columnas)

    df_result.to_sql(nombre_tabla, engine, if_exists='append', index=False)

#-------------------------------------------
#-------------------------------------------
#-------------------------------------------

def f_generar_grafica(nombre_archivo_db, nombre_imagen, palabras_entrenamiento):  #Genera la gráfica de dispersión. No devuelve nada.
    print("--- 📊 Generando gráfica ---")
    
    # Cargarmos los datos
    conn = sqlite3.connect(nombre_archivo_db)
    df = pd.read_sql_query("SELECT * FROM resultados", conn)
    conn.close()
    
    if df.empty:
        print("⚠️ La tabla 'resultados' está vacía. No se puede graficar.")
        return

    # print(f"   Datos cargados: {len(df)} partidas.")

    # Preparamos la Gráfica
    plt.figure(figsize=(10, 10)) # Tamaño cuadrado para que la diagonal sea de 45 grados reales

    # Calculamos el rango máximo para los ejes (para que quede simétrico)
    limite_max = max(df['intentos_fb'].max(), df['intentos_rf'].max()) + 2
    
    # Línea de Referencia (Empate técnico)
    plt.plot([0, limite_max], [0, limite_max], 
             color='black', linestyle='--', alpha=0.5, label='Línea de Empate (45º)')

    # Puntos donde Gana la IA (Verde)
    # Filtramos los datos donde RF necesitó menos intentos que la fuerza bruta
    gana_ia = df[df['intentos_rf'] < df['intentos_fb']]
    plt.scatter(gana_ia['intentos_fb'], gana_ia['intentos_rf'], 
                color='green', s=60, alpha=0.7, label=f'Gana IA ({len(gana_ia)})')

    # Puntos donde Gana Fuerza Bruta (Rojo)
    # Filtramos los datos donde RF necesitó más intentos que la fuerza bruta
    gana_fb = df[df['intentos_rf'] > df['intentos_fb']]
    plt.scatter(gana_fb['intentos_fb'], gana_fb['intentos_rf'], 
                color='#ff9999', s=60, alpha=0.7, label=f'Gana Fuerza Bruta ({len(gana_fb)})')

    # Puntos de Empate (Gris)
    empate = df[df['intentos_rf'] == df['intentos_fb']]
    if not empate.empty:
        plt.scatter(empate['intentos_fb'], empate['intentos_rf'], 
                    color='gray', s=60, alpha=0.5, label=f'Empate ({len(empate)})')

    # Decoración
    plt.title(f'IA ({int(palabras_entrenamiento/1000)}k palabras) vs Fuerza Bruta', fontsize=14, fontweight='bold')
    plt.xlabel('Intentos Fuerza Bruta', fontsize=12)
    plt.ylabel('Intentos Algoritmo IA', fontsize=12)
    
    plt.xlim(0, limite_max)
    plt.ylim(0, limite_max)
    plt.gca().set_aspect('equal', adjustable='box') # Fuerza que la relación de aspecto sea 1:1
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend() # Muestra la leyenda

    # Guardardamos la gráfica
    # print(f"💾 Guardando gráfica en '{nombre_imagen}'...")
    plt.tight_layout() # Ajusta los márgenes para que no se corten textos
    plt.savefig(nombre_imagen)
    print("✅ ¡Gráfica generada con éxito! Búscala en tu carpeta del proyecto.")

#-------------------------------------------
#-------------------------------------------
#-------------------------------------------
