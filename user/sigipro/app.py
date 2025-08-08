# ============================================================================
# SISTEMA DE INFORMACIÓN GEOGRÁFICA INTERCULTURAL (SIGIC)
# Aplicación Flask para gestión de comunidades indígenas
# ============================================================================

from flask import Flask
from routes.config import Config

# Importar blueprints
from routes.auth import auth_bp
from routes.main import main_bp
from routes.institucional import institucional_bp
from routes.proyectos import proyectos_bp
from routes.noticias import noticias_bp
from routes.usuarios import usuarios_bp
from routes.admin import admin_bp

def create_app():
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración de la aplicación
    app.secret_key = Config.SECRET_KEY
    app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(institucional_bp)
    app.register_blueprint(proyectos_bp)
    app.register_blueprint(noticias_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(admin_bp)
    
    return app

# Crear la aplicación
app = create_app()

# ============================================================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# ============================================================================

if __name__ == '__main__':
    """
    Punto de entrada principal de la aplicación Flask.
    
    Configuración de desarrollo:
    - host='0.0.0.0': Permite conexiones desde cualquier IP
    - port=5000: Puerto estándar de Flask
    - debug=True: Modo debug activado
    
    IMPORTANTE: En producción cambiar debug=False y usar un servidor WSGI
    """
    app.run(host='0.0.0.0', port=5000, debug=True)