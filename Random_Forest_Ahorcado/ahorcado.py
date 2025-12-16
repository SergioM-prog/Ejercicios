import time, random
from funciones import f_llamada_api, f_ejecutar_etl, f_entrenar_modelo, f_predecir_palabra, f_fuerza_bruta, f_guardar_resultados,f_generar_grafica

#=============================================#
#========= INTRUCCIONES IMPORTANTES ==========#
#=============================================#
# Dado que se trata de un ejercicio práctico, el script lo hace todo de golpe.
# Genera la tabla dataset de entrenamiento con los registros del número de palabras indicado en la variable NUM_PALABRAS_ENTRENAMIENTO (50k)
# Luego entrena el modelo Random Forest y lo prueba con palabras extraidas de la api de la RAE variable NUM_PALABRAS_RAE (100)
# Palabras_github.txt contiene 636.598 palabras para poder entrenar al modelo

# ============================================= #
# ========= CONFIGURACIÓN GENERAL ============= #
# ============================================= #

NUM_PALABRAS_ENTRENAMIENTO = 50000

NUM_PALABRAS_RAE = 100

RAE_URL="https://rae-api.com/api/random"
NOMBRE_ARCHIVO_DB = "ahorcado_data.db"
URL_DB = f"sqlite:///{NOMBRE_ARCHIVO_DB}"
TABLA_DATASET = 'dataset_ahorcado'
TABLA_RESULTADOS = 'resultados'
NOMBRE_IMAGEN = "comparativa_rendimiento.png"
ABECEDARIO = [
    'e', 'a', 'o', 'l', 's', 'n', 'r', 'i', 'd',
    'u', 't', 'c', 'm', 'p',
    'b', 'g', 'v', 'y', 'q', 'h', 'f',
    'j', 'ñ', 'x', 'z', 'k', 'w',
    'á', 'é', 'í', 'ó', 'ú', "ü"
        ]

# ============================================= #
# ========= ENTRENAMIENTO MODELO ============== #
# ============================================= #

t0 = time.time()

#Leemos el archivo .txt de las palabras de entrenamiento
with open("palabras_github.txt", 'r', encoding='utf-8') as f:
    palabras = [palabra.strip() for palabra in f]

#Estraemos de forma aleatoria el número de palabras definido
palabras_entrenamiento = random.sample(palabras, NUM_PALABRAS_ENTRENAMIENTO)

#Generamos el dataset
f_ejecutar_etl(palabras_entrenamiento,URL_DB, TABLA_DATASET,ABECEDARIO)

#Entrenamos el modelo con el dataset
clf = f_entrenar_modelo(URL_DB, TABLA_DATASET, ABECEDARIO)

# ============================================= #
# ============ PALABRAS DE PRUEBA ============= #
# ============================================= #

#Leemos el archivo .txt de las palabras de prueba
with open("palabras.txt", 'r', encoding='utf-8') as f:
    palabras_prueba = [palabra.strip() for palabra in f]


print(f"\n--- Iniciando palabras prueba ---\n")

contador_palabras = 0
intentos_algoritmo = 0
intentos_f_bruta = 0

#En este bucle resolvemos la palabra tanto con el algoritmo como por fuerza bruta
for palabra in palabras_prueba:

    palabra = palabra.lower()


    intentos_algoritmo += f_predecir_palabra(clf, palabra, ABECEDARIO, contador_palabras)
    intentos_f_bruta += f_fuerza_bruta(palabra)

    contador_palabras += 1

ahorro = intentos_f_bruta - intentos_algoritmo
porcentaje_mejora = (ahorro / 216) * 100

# Imprimimos resultados
if ahorro > 0:
    print(f"\n   TOTAL {contador_palabras} palabras: {intentos_algoritmo} intentos algoritmo. Mejora del {porcentaje_mejora:.2f}% frente a {intentos_f_bruta} intentos por fuerza bruta\n")
else:
    print(f"\n   TOTAL {contador_palabras} palabras: {intentos_algoritmo} intentos algoritmo. Empeoramiento del {abs(porcentaje_mejora):.2f}% frente a {intentos_f_bruta} intentos por fuerza bruta\n")

# ============================================= #
# =============== PALABRAS RAE ================ #
# ============================================= #

print(f"\n--- Iniciando palabras {NUM_PALABRAS_RAE} RAE ---\n")

contador_palabras = 0
lista_resultados = []

intentos_algoritmo = 0
intentos_f_bruta = 0

#En este bucle resolvemos las palabras de la RAE tanto con el algoritmo como por fuerza bruta. Tantas como las definidas en la variable NUM_PALABRAS_RAE.
#Pedimos una palabra a la api de la RAE cada 2 s, aprox. 30 por minuto. Se pueden pedir máximo 60 por minuto o 1000 al día.
while True:

    if contador_palabras == NUM_PALABRAS_RAE:
        break
    
    intentos_algoritmo_palabra = 0
    intentos_f_bruta_palabra = 0

    conexion_rae = f_llamada_api(RAE_URL,"rae")
    response = conexion_rae.json()
    palabra_rae = response["data"]["word"]

    intentos_algoritmo_palabra += f_predecir_palabra(clf,palabra_rae,ABECEDARIO,contador_palabras)
    intentos_algoritmo += intentos_algoritmo_palabra

    intentos_f_bruta_palabra += f_fuerza_bruta(palabra_rae)
    intentos_f_bruta += intentos_f_bruta_palabra

    lista_resultados.append((palabra_rae, len(palabra_rae), intentos_f_bruta_palabra, intentos_algoritmo_palabra))

    contador_palabras += 1

    time.sleep(2)

ahorro = intentos_f_bruta - intentos_algoritmo
porcentaje_mejora = (ahorro / intentos_f_bruta) * 100

# Imprimimos resultados

if ahorro > 0:
    print(f"\n   TOTAL {contador_palabras} palabras: {intentos_algoritmo} intentos algoritmo. Mejora del {porcentaje_mejora:.2f}% frente a {intentos_f_bruta} intentos por fuerza bruta\n")
else:
    print(f"\n   TOTAL {contador_palabras} palabras: {intentos_algoritmo} intentos algoritmo. Empeoramiento del {abs(porcentaje_mejora):.2f}% frente a {intentos_f_bruta} intentos por fuerza bruta\n")

# ============================================= #
# ============ ANALISIS RESULTADOS ============ #
# ============================================= #

#Guardamos los resultados en la TABLA_RESULTADOS y generamos la gráfica.
lista_columnas =["palabra", "longitud","intentos_fb","intentos_rf"]

f_guardar_resultados(URL_DB, lista_columnas, lista_resultados,TABLA_RESULTADOS)

f_generar_grafica(NOMBRE_ARCHIVO_DB, NOMBRE_IMAGEN, NUM_PALABRAS_ENTRENAMIENTO)

print(f"\nTIEMPO TOTAL: {int((time.time() - t0) // 60)} minutos y {int((time.time() - t0) % 60)} segundos.!")