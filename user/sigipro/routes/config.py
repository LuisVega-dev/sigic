class Config:
    """Configuración de la aplicación"""
    SECRET_KEY = 'secretkey'  # CAMBIAR EN PRODUCCIÓN
    UPLOAD_FOLDER = 'static/uploads'
    
    # Configuración de base de datos
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'charset': 'utf8mb4',
        'use_unicode': True,
        'database': 'sigic'
    }