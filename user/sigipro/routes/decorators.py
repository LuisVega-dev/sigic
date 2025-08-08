from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    """
    Decorador para proteger rutas que requieren autenticación.
    
    Este decorador verifica si existe una sesión activa de usuario.
    Si no la hay, redirige automáticamente a la página de login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.iniciar_sesion'))
        return f(*args, **kwargs)
    return decorated_function