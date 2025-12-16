import os, time, random
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import numpy as np
from funciones import (
    f_llamada_api, f_ejecutar_etl, f_entrenar_modelo, 
    f_predecir_palabra, f_fuerza_bruta, f_conexion_bd, 
    f_guardar_resultados
)

# ============================================= #
# ========= CONFIGURACIÓN GENERAL ============ #
# ============================================= #

MODEL_SIZES = [ 10000, 50000, 100000, 200000] 
NUM_PALABRAS_PRUEBA = 100

RAE_URL = "https://rae-api.com/api/random"
NOMBRE_ARCHIVO_DB = "ahorcado_data.db"
URL_DB = f"sqlite:///{NOMBRE_ARCHIVO_DB}"
TABLA_DATASET = 'dataset_ahorcado'
TABLA_RESULTADOS = 'resultados'
NOMBRE_IMAGEN = "comparativa_rendimiento_evolutiva.png"

ABECEDARIO = [
    'e', 'a', 'o', 'l', 's', 'n', 'r', 'i', 'd',
    'u', 't', 'c', 'm', 'p',
    'b', 'g', 'v', 'y', 'q', 'h', 'f',
    'j', 'ñ', 'x', 'z', 'k', 'w',
    'á', 'é', 'í', 'ó', 'ú', "ü"
]

# ============================================= #
# ========= 1. OBTENCIÓN DE PALABRAS ========= #
# ============================================= #

print("--- Cargando diccionario maestro ---")
with open("palabras_github.txt", 'r', encoding='utf-8') as f:
    palabras_totales = [palabra.strip() for palabra in f]

print(f"--- Obteniendo {NUM_PALABRAS_PRUEBA} palabras de la RAE para el set de pruebas ---")
lista_palabras_test = []

while len(lista_palabras_test) < NUM_PALABRAS_PRUEBA:
    try:
        conexion_rae = f_llamada_api(RAE_URL, "rae")
        response = conexion_rae.json()
        palabra_rae = response["data"]["word"].lower()
        
        if palabra_rae not in lista_palabras_test:
            lista_palabras_test.append(palabra_rae)
            print(f"  [{len(lista_palabras_test)}/{NUM_PALABRAS_PRUEBA}] Palabra obtenida: {palabra_rae}")
            time.sleep(2) 
    except Exception as e:
        print(f"Error conectando con RAE: {e}. Reintentando...")
        time.sleep(2)

# ============================================= #
# ========= 2. CÁLCULO FUERZA BRUTA ========== #
# ============================================= #

print("\n--- Ejecutando Fuerza Bruta (Baseline) ---")
resultados_consolidados = {}

for palabra in lista_palabras_test:
    intentos = f_fuerza_bruta(palabra)
    # IMPORTANTE: Aquí usamos 'intentos_fb' para que coincida con lo que espera tu sistema
    resultados_consolidados[palabra] = {
        'longitud': len(palabra),
        'intentos_fb': intentos 
    }

# ============================================= #
# ========= 3. BUCLE DE ENTRENAMIENTO ======== #
# ============================================= #

for size in MODEL_SIZES:
    key_modelo = f"rf_{int(size/1000)}k"
    print(f"\n=== INICIANDO CICLO: {size} palabras ({key_modelo}) ===")

    palabras_entrenamiento = random.sample(palabras_totales, size)
    
    # Ejecutamos ETL y Entrenamiento
    f_ejecutar_etl(palabras_entrenamiento, URL_DB, TABLA_DATASET, ABECEDARIO)
    clf = f_entrenar_modelo(URL_DB, TABLA_DATASET, ABECEDARIO)
    
    print(f"Evaluando modelo {key_modelo}...")
    
    intentos_totales_modelo = 0
    intentos_totales_fb = 0 

    for i, palabra in enumerate(lista_palabras_test):
        intentos = f_predecir_palabra(clf, palabra, ABECEDARIO, i)
        
        resultados_consolidados[palabra][key_modelo] = intentos
        
        intentos_totales_modelo += intentos
        intentos_totales_fb += resultados_consolidados[palabra]['intentos_fb']

    ahorro = intentos_totales_fb - intentos_totales_modelo
    base_calc = intentos_totales_fb if intentos_totales_fb > 0 else 1
    porcentaje = (ahorro / base_calc) * 100
    print(f"--> Mejora del modelo {key_modelo} sobre FB: {porcentaje:.2f}%")


# ============================================= #
# ========= 4. GUARDADO DE DATOS ============= #
# ============================================= #

print("\n--- Guardando resultados ---")

columnas_rf = [f"rf_{int(s/1000)}k" for s in MODEL_SIZES]
# Aquí corregimos el nombre de la columna para evitar el KeyError
lista_columnas = ["palabra", "longitud", "intentos_fb"] + columnas_rf

lista_resultados_final = []

for palabra, data in resultados_consolidados.items():
    fila = [
        palabra,
        data['longitud'],
        data['intentos_fb']
    ]
    for col in columnas_rf:
        fila.append(data[col])
    
    lista_resultados_final.append(tuple(fila))

f_guardar_resultados(URL_DB, lista_columnas, lista_resultados_final, TABLA_RESULTADOS)

# ============================================= #
# ========= 5. GENERACIÓN DE GRÁFICA ========= #
# ============================================= #
# NOTA: Hacemos la gráfica aquí localmente para soportar 
# las columnas dinámicas (1k, 10k, 50k...) que la función original no conoce.

print("--- Generando gráfica comparativa evolutiva ---")

try:
    # 1. Recuperar datos con Pandas
    conn = sqlite3.connect(NOMBRE_ARCHIVO_DB)
    query = f"SELECT * FROM {TABLA_RESULTADOS}"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # 2. Configurar el gráfico
    plt.figure(figsize=(14, 8))

    # Eje X: Las palabras
    x = df['palabra']

    # 3. Pintar Fuerza Bruta (Línea roja discontinua)
    plt.plot(x, df['intentos_fb'], label='Fuerza Bruta', color='red', linestyle='--', marker='o', alpha=0.6)

    # 4. Pintar cada modelo de Random Forest (Verdes progresivos)
    # Usamos un mapa de colores para que se vea la evolución
    colors = plt.cm.Greens(np.linspace(0.4, 1, len(columnas_rf)))

    for i, col_name in enumerate(columnas_rf):
        if col_name in df.columns:
            plt.plot(x, df[col_name], label=f'Random Forest {col_name}', color=colors[i], marker='o', linewidth=2)

    # 5. Estética
    plt.title(f'Evolución de Eficiencia: Fuerza Bruta vs IA (Entrenamiento incremental)', fontsize=16)
    plt.xlabel('Palabras (RAE)', fontsize=12)
    plt.ylabel('Intentos Necesarios', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()

    # 6. Guardar
    plt.savefig(NOMBRE_IMAGEN)
    print(f"✅ Gráfica generada correctamente: {NOMBRE_IMAGEN}")

except Exception as e:
    print(f"❌ Error generando la gráfica manual: {e}")