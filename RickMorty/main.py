import os, psycopg, requests
# import matplotlib.pyplot as plt

#=============================================#
#=========== CONEXIÓN A LA BD ================#
#=============================================#


#--------URL CONEXIÓN A BD --------
url = os.getenv("DATABASE_URL")                  #Accede a la variable de entorno DATABASE_URL

#--------CONEXIÓN A BD con intentos--------

# Número máximo de intentos
max_reintentos = 10
espera_segundos = 3

# Intentar conectar con reintentos
for intento in range(1, max_reintentos + 1):
    try:
        connection = psycopg.connect(url)
        print("✅ Conexión exitosa a la base de datos")
        break
    except psycopg.OperationalError as e:
        print(f"❌ Intento {intento}: la base de datos no está lista aún.")
        if intento == max_reintentos:
            print("🚨 Se alcanzó el número máximo de reintentos. Abortando.")
            raise e                                                             #- vuelve a lanzar eL mismo error
        time.sleep(espera_segundos)

#--------Cursor--------
cur = connection.cursor()

#=============================================#
#=========== CREACIÓN TABLA ==================#
#=============================================#

cur.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY,
                name TEXT,
                status TEXT,
                species TEXT,
                type TEXT,
                gender TEXT,
                origin_name TEXT,
                location_name TEXT,
                image TEXT,
                url TEXT,
                created TIMESTAMPTZ
            );
        """)

#=============================================#
#=========== LLAMADA A LA API ================#
#=============================================#

url = "https://rickandmortyapi.com/api/character"
response = requests.get(url)

#=============================================#
#=========== RECORRIDO POR PÁGINA ============#
#=============================================#

# La API de Rick y Morty está estruturada por páginas. En total son 42 páginas de 20 personajes cada una.
# Cada página está compuesta por un diccionario que contiene dos Keys: "info" y "results"
# info es un diccionario que contiene metadatos de la paginación: "count": 826, --> "pages": 42, ....
# results es una lista de diccionarios que a su vez contienen la información de cada personaje
# En esta parte del código se va a iterar por cada página, se creará una tupla vacía y se llenará con la información de cada personaje
# Cuando termine de recorrer una página subirá los datos de la tupla a la BD y pasará a recorrer la siguiente página.
# En términos de eficiencia, escalabilidad y manejo de errores, es más recomendable procesar e insertar los datos página por página, en lugar de acumular todas las páginas en memoria y luego hacer un único INSERT.


rm_pages = int(os.getenv("RM_PAGES", 1))                                    # Recupera la variable de entorno RM_PAGES. Usa 1 por defecto si no está definida

for page in range(1, rm_pages + 1):

    url = f"https://rickandmortyapi.com/api/character?page={page}"
    response = requests.get(url)

    if response.status_code != 200:                                         # Verifica si la respuesta fue exitosa Código HTTP (200 = OK, 404 = no encontrado…)
        print(f"❌ Error en la página {page}: {response.status_code}")
        continue
    data = response.json()

    personajes = []                                                         # Crea una tupla vacía donde llenaremos los personajes del diccionario results. executemany() sólo acepta una tupla

    for p in data["results"]:                                               # Recorre la lista results para guardar en la tupla vacía cada personaje
        personajes.append((
            p["id"],
            p["name"],
            p["status"],
            p["species"],
            p["type"],
            p["gender"],
            p["origin"]["name"],
            p["location"]["name"],
            p["image"],
            p["url"],
            p["created"]
        ))
    # Carga en la BD los datos de la tupla personajes
    cur.executemany("""
        INSERT INTO characters (
            id, name, status, species, type, gender,
            origin_name, location_name, image, url, created
        ) VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        ON CONFLICT (id) DO NOTHING;
    """, personajes)

    connection.commit()
    print(f"✅ Página {page} procesada con {len(personajes)} personajes")

cur.execute("SELECT id, name, species FROM characters LIMIT 10;")
print(cur.fetchall())

cur.execute("SELECT COUNT(*) FROM characters;")
total = cur.fetchone()[0]
print(f"📊 Total de personajes en la base de datos: {total}")


#=============================================#
#==== VISUALIZACIÓN DE DATOS MATPLOTLIB ======#
# #=============================================#

# cur.execute("SELECT species, COUNT(*) FROM characters GROUP BY species;")
# rows = cur.fetchall()

# species = [r[0] for r in rows]
# counts = [r[1] for r in rows]

# plt.bar(species, counts)
# plt.title("Número de personajes por especie")
# plt.xlabel("Especie")
# plt.ylabel("Cantidad")
# plt.xticks(rotation=45, ha="right")
# plt.tight_layout()
# plt.savefig("grafico.png")

# print("✅ Gráfico guardado como grafico.png")

# cur.close()
# connection.close()