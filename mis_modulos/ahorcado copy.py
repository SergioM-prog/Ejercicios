import os, sys, time
from funciones import f_conexion_bd, f_llamada_api, f_dataset_extend, f_dataset_basic, f_carga_batch, f_entrenamiento, f_probar_palabra



#=============================================#
#========= INTRUCCIONES IMPORTANTES ==========#
#=============================================#
# Dado que se trata de un ejercicio práctico, el script lo hace todo de golpe.
# Genera la tabla dataset de entrenamiento con los registros del número de palabras indicado en la variable num_palabras_entrenamiento
# y entrena el modelo ramdon forest todo seguido
# Palabras.txt contiene 636.598 palabras para poder entrenar al modelo
# El proceso completo para 10.000 palabras tarda aprox, 1m 20s y genera 164.238 registros de partidas simuladas
# El proceso completo para 20.000 palabras tarda aprox, 3m 20s y genera 325.706 registros de partidas simuladas
# Los registros se cargarán en el dataset en bloques de tamaño definido en la variable batch_size


batch_size = 50000
num_palabras_entrenamiento = 1000
modelo_probar = 0                   #0 para probar el modelo entrenado con el dataset básico, 1 para probar el extendido

#URL CONEXIÓN A BD. Definida en la variable de entorno DATABASE_URL del .env

url_ahorcado = os.getenv("DATABASE_URL")

#CONEXIÓN A BD con intentos y tiempo de espera

conexion_ahorcado = f_conexion_bd(url_ahorcado,"ahorcado")

# Cursor.
# Crea un cursor, que es un objeto que permite ejecutar comandos SQL.
# - El cursor es como un "canal" entre tu código y la base de datos: puedes enviar consultas (SELECT, INSERT, etc.) y recibir resultados.
cur = conexion_ahorcado.cursor()
print("Cursor creado con éxito")

#=============================================#
#=========== CREACIÓN TABLAS =================#
#=============================================#

if modelo_probar == 1:

    cur.execute("""
        CREATE TABLE IF NOT EXISTS dataset_extend (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
            palabra TEXT,
            longitud_palabra INT,
            tiene_tilde BOOLEAN,
            tiene_ñ BOOLEAN,
            num_vocales INT,
            num_consonantes INT,
            letras_unicas INT,
            frecuencia_letras FLOAT,
            letra_probada TEXT,
            letras_acertadas TEXT,
            letras_falladas TEXT,
            intentos INT,
            acierto BOOLEAN
        );
    """)

elif modelo_probar == 0:

    cur.execute("""
        CREATE TABLE IF NOT EXISTS dataset_basic (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
            palabra TEXT,
            longitud_palabra INT,
            letras_unicas INT,
            letra_probada TEXT,
            letras_acertadas TEXT,
            letras_falladas TEXT,
            intentos INT,
            acierto BOOLEAN
        );
    """)

conexion_ahorcado.commit()
print("Tablas creadas con éxito en la BD")


# #--------------------------
# archivo = sys.argv[1]  # toma el primer argumento después del nombre del script

#Lee el archivo .txt
with open("palabras_github.txt", 'r', encoding='utf-8') as f:
    palabras = [palabra.strip() for palabra in f]


lista_registros = []    # lista de tuplas de registros
palabras_entrenamiento = palabras[:num_palabras_entrenamiento]

print(f"Generando los registros para {num_palabras_entrenamiento} palabras")


if modelo_probar == 0:

    for palabra in palabras_entrenamiento:
        lista_registros.extend(f_dataset_basic(palabra))

elif modelo_probar == 1:

    for palabra in palabras_entrenamiento:
        lista_registros.extend(f_dataset_extend(palabra))

num_registros = len(lista_registros)
print(f"Total de registros generados: {num_registros}")

# Cargamos a la BD los registros poco a poco, en bloques del tamaño definido en la variable batch_size

f_carga_batch(lista_registros,batch_size,modelo_probar,conexion_ahorcado,cur)

#Entrenamos el modelo

clf = f_entrenamiento(modelo_probar)

f_probar_palabra(clf,"Xilófono")

cur.close()
conexion_ahorcado.close()

# while True:

#     url_rae = os.getenv("RAE_URL")
#     conexion_rae = f_llamada_api(url_rae,"rae")
#     response = conexion_rae.json()
#     palabra_rae = response["data"]["word"]

#     lista_registros = f_adivinar_palabra(palabra_rae)
#     cur.executemany("INSERT INTO ahorcado (palabra, letras_acertadas, letras_falladas, intentos, tiempo) VALUES (%s, %s, %s, %s, %s)", lista_registros)
#     conexion_ahorcado.commit()

#     time.sleep(10)



