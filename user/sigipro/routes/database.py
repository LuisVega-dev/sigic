import pymysql
from .config import Config

def get_db_connection():
    """
    Establece y retorna una conexión a la base de datos MySQL.
    
    Returns:
        pymysql.Connection: Objeto de conexión configurado para retornar 
                           resultados como diccionarios en lugar de tuplas.
    """
    return pymysql.connect(
        **Config.DB_CONFIG,
        cursorclass=pymysql.cursors.DictCursor,
    )