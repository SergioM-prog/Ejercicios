import psycopg, requests, time, os
from datetime import datetime
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sqlalchemy import create_engine
from sklearn.metrics import classification_report


def f_conexion_bd(db_url, db_nombre):
    for i in range(10):
        try:            
            connection = psycopg.connect(db_url)
            print(f"BD {db_nombre} conectada con éxito")
            return connection
        
        except psycopg.OperationalError as e:
            print(f"Intento {i+1}: la BD {db_nombre} aún no está lista. Esperando...")
            time.sleep(2)
    raise RuntimeError(f"No se pudo conectar a la BD {db_nombre} tras 10 intentos")


def f_llamada_api(api_url, api_nombre):
    for i in range(10):
        try:
            
            response = requests.get(api_url)
            print(f"API {api_nombre} conectada con éxito")
            return response
        
        except requests.exceptions.RequestException as e:
            print(f"Intento {i+1}: la API {api_nombre} aún no está lista. Esperando...")
            time.sleep(2)
    raise RuntimeError(f"No se pudo conectar a la API {api_nombre} tras 10 intentos")

def f_dataset_basic(palabra):

    abecedario = [
    'e', 'a', 'o', 'l', 's', 'n', 'r', 'i', 'd',
    'u', 't', 'c', 'm', 'p',
    'b', 'g', 'v', 'y', 'q', 'h', 'f',
    'j', 'ñ', 'x', 'z', 'k', 'w',
    'á', 'é', 'í', 'ó', 'ú'
        ]
    palabra_minusculas = palabra.lower()
    letras_unicas = len(set(palabra_minusculas))
    contador_letras_acertadas = 0
    letras_acertadas = ""
    letras_falladas = ""
    lista_registros = []    # lista de tuplas de registros
    intentos = 0
    longitud_palabra = len(palabra)
    acierto = False


    for letra in abecedario:

        if contador_letras_acertadas == letras_unicas:
            break

        else:

            if letra in palabra_minusculas:

                letras_acertadas += letra
                contador_letras_acertadas += 1
                intentos += 1
                acierto = True
                lista_registros.append((palabra, longitud_palabra, letras_unicas, letra, letras_acertadas, letras_falladas, intentos, acierto))
                
                continue           

            else:

                letras_falladas += letra
                intentos += 1
                acierto = False
                lista_registros.append((palabra, longitud_palabra, letras_unicas, letra, letras_acertadas, letras_falladas, intentos, acierto))
                
                continue

    return lista_registros


def f_dataset_extend(palabra):

    abecedario = [
    'e', 'a', 'o', 'l', 's', 'n', 'r', 'i', 'd',
    'u', 't', 'c', 'm', 'p',
    'b', 'g', 'v', 'y', 'q', 'h', 'f',
    'j', 'ñ', 'x', 'z', 'k', 'w',
    'á', 'é', 'í', 'ó', 'ú'
        ]
    palabra_minusculas = palabra.lower()
    letras_unicas = len(set(palabra_minusculas))
    contador_letras_acertadas = 0
    letras_acertadas = ""
    letras_falladas = ""
    lista_registros = []    # lista de tuplas de registros
    intentos = 0
    vocales = "aeiouáéíóú"
    tildes = "áéíóú"
    longitud_palabra = len(palabra)
    tiene_tilde = False
    tiene_n = False
    num_vocales = 0
    num_consonantes = 0
    frecuencia_letras = 0.0     #vocales/longitud
    acierto = False

    for letra in palabra:
        if letra in tildes:         tiene_tilde = True
        if letra =="ñ":             tiene_n = True
        if letra in vocales:        num_vocales += 1

    num_consonantes = longitud_palabra - num_vocales
    frecuencia_letras = num_vocales/longitud_palabra

    for letra in abecedario:

        if contador_letras_acertadas == letras_unicas:
            break

        else:

            if letra in palabra_minusculas:

                letras_acertadas += letra
                contador_letras_acertadas += 1
                intentos += 1
                acierto = True
                lista_registros.append((palabra, longitud_palabra, tiene_tilde, tiene_n, num_vocales, num_consonantes, letras_unicas, frecuencia_letras, letra, letras_acertadas, letras_falladas, intentos, acierto))
                
                continue           

            else:

                letras_falladas += letra
                intentos += 1
                acierto = False
                lista_registros.append((palabra, longitud_palabra, tiene_tilde, tiene_n, num_vocales, num_consonantes, letras_unicas, frecuencia_letras, letra, letras_acertadas, letras_falladas, intentos, acierto))
                
                continue

    return lista_registros


def f_carga_batch(lista_registros,batch_size,modelo_probar,conexion_ahorcado,cur):

    registros_cargados = 0
    num_registros = len(lista_registros)

    if modelo_probar == 0:              #dataset básico

        for i in range(0, len(lista_registros), batch_size):
            batch = lista_registros[i:i+batch_size]
            cur.executemany("""
                INSERT INTO dataset_basic (
                    palabra,
                    longitud_palabra,
                    letras_unicas,
                    letra_probada,
                    letras_acertadas,
                    letras_falladas,
                    intentos,
                    acierto
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, batch)
            registros_cargados += len(batch)
            conexion_ahorcado.commit()
            print(f"Total de registros cargados en la BD: {registros_cargados} de {num_registros}")

    elif modelo_probar ==1:         #dataset extendido

        for i in range(0, len(lista_registros), batch_size):
            batch = lista_registros[i:i+batch_size]
            cur.executemany("""
                INSERT INTO dataset_extend (
                    palabra,
                    longitud_palabra,
                    tiene_tilde,
                    tiene_ñ,
                    num_vocales,
                    num_consonantes,
                    letras_unicas,
                    frecuencia_letras,
                    letra_probada,
                    letras_acertadas,
                    letras_falladas,
                    intentos,
                    acierto
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, batch)
            registros_cargados += len(batch)
            conexion_ahorcado.commit()
            print(f"Total de registros cargados en la BD: {registros_cargados} de {num_registros}")

def f_entrenamiento (modelo_probar):

    url_ahorcado_pandas = os.getenv("DATABASE_URL_PANDAS") #Se utiliza una URL diferente para conectar a la BD con pandas para usar psycopg en lugar de psycopg2 que coge por defecto. Como no está instalado psycopg2, el import falla y el contenedor se cae.
    
    if modelo_probar == 1:
    
        query = "SELECT * FROM dataset_extend;"
        engine = create_engine(url_ahorcado_pandas)    # Para la conexión a la BD con grandes volúmenes, pandas no trabaja bien con objetos psycopg.Connection. Por eso se utiliza create_engine de la librería sqlalchemy

        df = pd.read_sql(query, engine)


        # Definimos las features y el target"
        X = df[[
            "longitud_palabra",
            "tiene_tilde",
            "tiene_ñ",
            "num_vocales",
            "num_consonantes",
            "letras_unicas",
            "frecuencia_letras",
            "letra_probada",
            "letras_acertadas",
            "letras_falladas",
            "intentos"
        ]]

        y = df["acierto"]

        # Crear el encoder para transformar las columnas que son string en columnas numéricas.
        encoder = OneHotEncoder(handle_unknown="ignore")

        # Ajustar y transformar
        columnas_string = ["letra_probada", "letras_acertadas", "letras_falladas"]
        columnas_numericas = ["longitud_palabra", "num_vocales", "num_consonantes", "letras_unicas", "frecuencia_letras", "intentos"]
        columnas_booleanas = ["tiene_tilde", "tiene_ñ"]


        # Preprocesador: aplica OneHotEncoder (Para convertir las columnas string en numéricas) a las columnas string y deja pasar las demás
        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore"), columnas_string),
                ("num", "passthrough", columnas_numericas),
                ("bool", "passthrough", columnas_booleanas)
            ]
        )

        # Dividimos en train/test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Pipeline con preprocesador y modelo
        clf = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("model", RandomForestClassifier(n_estimators=100, random_state=42))
        ])

        # Entrenamos
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        print(classification_report(y_test, y_pred))

    elif modelo_probar == 0:
                
        query = "SELECT * FROM dataset_basic;"
        engine = create_engine(url_ahorcado_pandas)    # Para la conexión a la BD con grandes volúmenes, pandas no trabaja bien con objetos psycopg.Connection. Por eso se utiliza create_engine de la librería sqlalchemy

        df = pd.read_sql(query, engine)


        # Definimos las features y el target"
        X = df[[
            "longitud_palabra",
            "letras_unicas",
            "letra_probada",
            "letras_acertadas",
            "letras_falladas",
            "intentos"
        ]]

        y = df["acierto"]

        # Crear el encoder para transformar las columnas que son string en columnas numéricas.
        encoder = OneHotEncoder(handle_unknown="ignore")

        # Ajustar y transformar
        columnas_string = ["letra_probada", "letras_acertadas", "letras_falladas"]
        columnas_numericas = ["longitud_palabra", "letras_unicas", "intentos"]


        # Preprocesador: aplica OneHotEncoder (Para convertir las columnas string en numéricas) a las columnas string y deja pasar las demás
        preprocessor = ColumnTransformer(
            transformers=[
                ("cat", OneHotEncoder(handle_unknown="ignore"), columnas_string),
                ("num", "passthrough", columnas_numericas)
            ]
        )

        # Dividimos en train/test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Pipeline con preprocesador y modelo
        clf = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("model", RandomForestClassifier(n_estimators=100, random_state=42))
        ])

        # Entrenamos
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        print(classification_report(y_test, y_pred))
    
    return clf

def f_probar_palabra(clf, palabra):

    abecedario = [
    'e', 'a', 'o', 'l', 's', 'n', 'r', 'i', 'd',
    'u', 't', 'c', 'm', 'p',
    'b', 'g', 'v', 'y', 'q', 'h', 'f',
    'j', 'ñ', 'x', 'z', 'k', 'w',
    'á', 'é', 'í', 'ó', 'ú'
        ]
    palabra = palabra.lower()
    letras_acertadas = ""        #El tipo set no admite carácteres duplicados
    letras_falladas = ""
    intentos = 0

    for letra in abecedario:

        if len(letras_acertadas) == len(set(palabra)): break

        registro = {
            "longitud_palabra": len(palabra),
            "letras_unicas": len(set(palabra)),
            "letra_probada": letra,
            "letras_acertadas": letras_acertadas, # convertir set a string para que no pete el OneHotEncoder que sólo admite strings
            "letras_falladas": letras_falladas,
            "intentos": intentos
        }

        X_test = pd.DataFrame([registro])
        pred = clf.predict(X_test)[0]

        if pred == 1:  # acierto

            if letra in palabra:

                letras_acertadas.add(letra)
                print(f"Acierto con la letra '{letra}'")

            else:
                letras_falladas.add(letra)
                print(f"Fallo con la letra '{letra}'")
            intentos += 1

        else:     # fallo
            continue

    print(f"Palabra: {palabra}")
    print(f"Letras acertadas: {letras_acertadas}")
    print(f"Letras falladas: {letras_falladas}")
    print(f"Intentos: {intentos}")