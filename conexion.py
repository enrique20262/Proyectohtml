import pymysql

import os

# Intentar parsear el puerto de manera segura
try:
    db_port = int(os.environ.get('DB_PORT', '3306'))
except ValueError:
    db_port = 3306

# Configuración con variables de entorno para Deploy y fallback local
CONFIG_DB = {
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'Ratalada2024'),
    'database': os.environ.get('DB_DATABASE', 'safecampus'),
    'port': db_port
}

# 1. Función de conexión básica
def obtener_conexion():
    return pymysql.connect(**CONFIG_DB, cursorclass=pymysql.cursors.DictCursor)

# 2. Función corregida para aceptar el parámetro 'fetch' que pide login.py
def ejecutar_query(sql, params=None, fetch=False):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(sql, params or ())
            if fetch:
                return cursor.fetchall()
            conexion.commit()
    finally:
        conexion.close()