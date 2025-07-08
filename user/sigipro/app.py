from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, Email
import os
import pymysql

app = Flask(__name__)
# Clave secreta para las sesiones (cambiar en producción)
app.secret_key = 'secretkey'

# ============================================================================
# CONEXIÓN A LA BASE DE DATOS
# ============================================================================

def get_db_connection():
    """
    Establece y retorna una conexión a la base de datos MySQL.
    Configurada para retornar resultados como diccionarios.
    """
    return pymysql.connect(
        host='localhost',        # Servidor de base de datos
        user='root',            # Usuario de MySQL
        password='',            # Contraseña (vacía en XAMPP por defecto)
        charset='utf8mb4',      # Codificación de caracteres
        use_unicode=True,       # Soporte para Unicode
        database='sigic',       # Nombre de la base de datos
        cursorclass=pymysql.cursors.DictCursor,  # Resultados como diccionarios
    )

# ============================================================================

# Decorador para proteger las rutas que requieren inicio de sesión
def login_required(f):
    """
    Decorador que verifica si el usuario ha iniciado sesión.
    Si no hay sesión activa, redirige al login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si existe una sesión de administrador activa
        if 'user_id' not in session:
            return redirect(url_for('iniciar_sesion'))
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# RUTAS DE AUTENTICACIÓN Y SESIÓN
# ============================================================================

# Login - Ruta para el inicio de sesión de administradores
@app.route('/iniciar-sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    # Si es una petición POST, procesar los datos del formulario de login
    if request.method == 'POST':
        # Obtener el correo y contraseña del formulario
        correo = request.form['correo']
        password = request.form['contraseña']
        
        try:
            # Conectar a la base de datos
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Buscar el usuario por correo electrónico
            cur.execute("SELECT * FROM usuario WHERE correo=%s", (correo,))
            user = cur.fetchone()
            
            # Cerrar la conexión a la base de datos
            cur.close()
            conn.close()
            
            # Verificar si el usuario existe y la contraseña es correcta
            if user and check_password_hash(user['contraseña'], password):
                # Crear la sesión del administrador
                session['user_id'] = user['id']
                session['user_name'] = user['nombre']
                session['usuario'] = user['nombre']  # Para compatibilidad con plantillas
                session['user_image'] = user.get('imagen')  # Guardar la imagen en sesión
                
                flash("Inicio de sesión exitoso", 'success')
                return redirect(url_for('inicio_privado'))
            else:
                # Usuario no encontrado o contraseña incorrecta
                flash("Usuario o contraseña incorrecta", 'danger')
                return redirect(url_for('iniciar_sesion'))
        except Exception as e:
            # Manejar errores de base de datos u otros errores
            flash(f"Error al iniciar sesión: {e}", 'danger')
            return redirect(url_for('iniciar_sesion'))
    
    # Si es una petición GET, mostrar el formulario de login
    return render_template('login.html')

# Ruta raíz
@app.route('/')
def inicio():
    if 'user_id' in session:
        return redirect(url_for('inicio_privado'))
    return render_template('index.html')
# Ruta para cerrar sesión
@app.route('/cerrar-sesion')
def cerrar_sesion():
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('iniciar_sesion'))

# Ruta de registro (temporal - para evitar errores)
@app.route('/registro')
def registro():
    return render_template('registro.html')

# Ruta de contacto
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        # Procesar formulario de contacto
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        mensaje = request.form.get('mensaje')
        
        # Aquí podrías guardar en base de datos o enviar email
        flash('¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.', 'success')
        return redirect(url_for('contacto'))
    
    return render_template('contacto.html')

# Rutas adicionales para las páginas del menú
@app.route('/sigic')
@login_required
def inicio_privado():
    # Obtener actividades recientes (datos de ejemplo por ahora)
    actividades = [
        {
            'fecha_hora': datetime.now(),
            'accion': 'Inicio de sesión exitoso',
            'usuario': session.get('user_name', 'Usuario')
        },
        {
            'fecha_hora': datetime.now() - timedelta(hours=2),
            'accion': 'Visualización de proyectos',
            'usuario': session.get('user_name', 'Usuario')
        },
        {
            'fecha_hora': datetime.now() - timedelta(days=1),
            'accion': 'Actualización de perfil',
            'usuario': session.get('user_name', 'Usuario')
        }
    ]
    
    # Agregar usuario a la sesión para compatibilidad con la plantilla
    session['usuario'] = session.get('user_name', 'Usuario')
    
    return render_template('inicio_privado.html', actividades=actividades)

@app.route('/sobre-nosotros')
@login_required
def sobre_nosotros():
    return render_template('sobre_nosotros.html')

@app.route('/equipo')
@login_required
def equipo():
    return render_template('equipo.html')

@app.route('/territorio')
@login_required
def territorio():
    return render_template('territorio.html')

@app.route('/cosmovision')
@login_required
def cosmovision():
    return render_template('cosmovision.html')

@app.route('/objetivos')
@login_required
def objetivos():
    return render_template('objetivos.html')

@app.route('/mision')
@login_required
def mision():
    return render_template('mision.html')

@app.route('/identidad')
@login_required
def identidad():
    return render_template('identidad.html')

@app.route('/mision-espiritual')
@login_required
def mision_espiritual():
    return render_template('mision_espiritual.html')

@app.route('/modulo')
@login_required
def modulo():
    return render_template('modulo.html')

@app.route('/historia')
@login_required
def historia():
    return render_template('historia.html')

@app.route('/proyectos')
def proyectos():
    return render_template('proyectos.html')

@app.route('/proyecto/<int:id>')
def ver_proyecto(id):
    # Datos de ejemplo - deberías obtener de la base de datos
    proyecto = {'id': id, 'titulo': 'Proyecto de ejemplo', 'descripcion': 'Descripción del proyecto'}
    return render_template('ver_proyecto.html', proyecto=proyecto)

@app.route('/noticias')
def noticias():
    return render_template('noticias.html')

@app.route('/noticia/<int:id>')
def ver_noticia(id):
    # Datos de ejemplo - deberías obtener de la base de datos
    noticia = {'id': id, 'titulo': 'Noticia de ejemplo', 'contenido': 'Contenido de la noticia'}
    return render_template('ver_noticia.html', noticia=noticia)

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

# Rutas adicionales que podrían estar referenciadas
@app.route('/editar-perfil')
@login_required
def editar_perfil():
    return render_template('editar_perfil.html')

@app.route('/agregar-proyecto')
@login_required
def agregar_proyecto():
    return render_template('agregar_proyecto.html')

@app.route('/editar-proyecto/<int:id>')
@login_required
def editar_proyecto(id):
    return render_template('editar_proyecto.html')

@app.route('/agregar-noticia')
@login_required
def agregar_noticia():
    return render_template('agregar_noticia.html')

@app.route('/editar-noticia/<int:id>')
@login_required
def editar_noticia(id):
    return render_template('editar_noticia.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)