import os, psycopg

#URL CONEXIÓN A BD. Definida en la variable de entorno DATABASE_URL del .env
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor.
# Crea un cursor, que es un objeto que permite ejecutar comandos SQL.
# - El cursor es como un "canal" entre tu código y la base de datos: puedes enviar consultas (SELECT, INSERT, etc.) y recibir resultados.
cur = connection.cursor()
print("BD conectada con éxito")