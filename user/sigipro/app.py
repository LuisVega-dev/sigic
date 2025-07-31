# ============================================================================
# SISTEMA DE INFORMACIÓN GEOGRÁFICA INTERCULTURAL (SIGIC)
# Aplicación Flask para gestión de comunidades indígenas
# ============================================================================

# Importaciones necesarias para Flask y funcionalidades
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash  # Para encriptar contraseñas
from functools import wraps  # Para crear decoradores personalizados
from datetime import datetime, timedelta  # Para manejo de fechas y tiempo
from werkzeug.utils import secure_filename  # Para nombres de archivo seguros
from flask_wtf import FlaskForm  # Para formularios seguros con CSRF protection
from wtforms import StringField, FileField, SubmitField, PasswordField, EmailField  # Campos de formulario
from wtforms.validators import DataRequired, Email, EqualTo  # Validadores de formulario
import os  # Para operaciones del sistema operativo
import pymysql  # Driver para conexión directa con MySQL

# Inicialización de la aplicación Flask
app = Flask(__name__)
# Clave secreta para firmar cookies de sesión y tokens CSRF (CAMBIAR EN PRODUCCIÓN)
app.secret_key = 'secretkey'
# Configuración de la carpeta para subir imágenes
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ============================================================================
# FORMULARIOS CON FLASK-WTF
# ============================================================================

class RegistroForm(FlaskForm):
    """
    Formulario para registro de nuevos usuarios con validación y protección CSRF.
    """
    nombre = StringField('Nombre completo', validators=[DataRequired(message='El nombre es obligatorio')])
    correo = EmailField('Correo electrónico', validators=[
        DataRequired(message='El correo es obligatorio'),
        Email(message='Ingresa un correo válido')
    ])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(message='La contraseña es obligatoria')])
    confirmar_contraseña = PasswordField('Confirmar contraseña', validators=[
        DataRequired(message='Confirma tu contraseña'),
        EqualTo('contraseña', message='Las contraseñas deben coincidir')
    ])
    imagen = FileField('Imagen de perfil (opcional)')
    submit = SubmitField('Registrarse')

# ============================================================================
# CONFIGURACIÓN DE BASE DE DATOS
# ============================================================================

def get_db_connection():
    """
    Establece y retorna una conexión a la base de datos MySQL.
    
    Returns:
        pymysql.Connection: Objeto de conexión configurado para retornar 
                           resultados como diccionarios en lugar de tuplas.
                           
    Raises:
        pymysql.Error: Si hay problemas de conexión con la base de datos.
        
    Note:
        Configuración para XAMPP local:
        - Host: localhost
        - Usuario: root (usuario por defecto de XAMPP)
        - Contraseña: '' (vacía por defecto en XAMPP)
        - Base de datos: sigic
        - Codificación: utf8mb4 (soporte completo para Unicode)
    """
    return pymysql.connect(
        host='localhost',        # Servidor de base de datos
        user='root',            # Usuario de MySQL
        password='',            # Contraseña (vacía en XAMPP por defecto)
        charset='utf8mb4',      # Codificación de caracteres para soporte Unicode completo
        use_unicode=True,       # Habilitar soporte para Unicode
        database='sigic',       # Nombre de la base de datos
        cursorclass=pymysql.cursors.DictCursor,  # Resultados como diccionarios
    )

# ============================================================================
# DECORADORES DE SEGURIDAD
# ============================================================================

def login_required(f):
    """
    Decorador para proteger rutas que requieren autenticación.
    
    Este decorador verifica si existe una sesión activa de usuario.
    Si no la hay, redirige automáticamente a la página de login.
    
    Args:
        f (function): La función de vista que se va a proteger.
        
    Returns:
        function: La función decorada que incluye la verificación de sesión.
        
    Usage:
        @app.route('/ruta-protegida')
        @login_required
        def ruta_protegida():
            return "Solo usuarios autenticados pueden ver esto"
    """
    @wraps(f)  # Preserva metadatos de la función original
    def decorated_function(*args, **kwargs):
        # Verificar si existe una sesión de usuario activa
        if 'user_id' not in session:
            # Si no hay sesión, redirigir al login
            return redirect(url_for('iniciar_sesion'))
        # Si hay sesión activa, continuar con la función original
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# RUTAS DE AUTENTICACIÓN Y GESTIÓN DE SESIONES
# ============================================================================

@app.route('/iniciar-sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    """
    Maneja el proceso de inicio de sesión de usuarios.
    
    GET: Muestra el formulario de login
    POST: Procesa las credenciales y crea la sesión del usuario
    
    Returns:
        GET: Renderiza la plantilla de login (login.html)
        POST: Redirige a inicio_privado si es exitoso, o de vuelta al login si falla
        
    Form Data (POST):
        correo (str): Correo electrónico del usuario
        contraseña (str): Contraseña en texto plano (se verifica contra hash almacenado)
        
    Session Variables Created:
        user_id (int): ID único del usuario en la base de datos
        user_name (str): Nombre del usuario
        usuario (str): Alias del nombre para compatibilidad con plantillas
        user_image (str): Ruta de la imagen de perfil del usuario
    """
    # Si es una petición POST, procesar los datos del formulario de login
    if request.method == 'POST':
        # Obtener las credenciales del formulario
        correo = request.form['correo']
        password = request.form['contraseña']
        
        try:
            # Establecer conexión con la base de datos
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Buscar el usuario por correo electrónico en la tabla 'usuario'
            cur.execute("SELECT * FROM usuario WHERE correo=%s", (correo,))
            user = cur.fetchone()
            
            # Cerrar la conexión para liberar recursos
            cur.close()
            conn.close()
            
            # Verificar si el usuario existe y la contraseña es correcta
            if user and check_password_hash(user['contraseña'], password):
                # Crear la sesión del usuario (equivalente a "iniciar sesión")
                session['user_id'] = user['id']
                session['user_name'] = user['nombre']
                session['usuario'] = user['nombre']  # Para compatibilidad con plantillas legacy
                session['user_image'] = user.get('imagen')  # Imagen de perfil (puede ser None)
                
                # Notificar éxito al usuario
                flash("Inicio de sesión exitoso", 'success')
                return redirect(url_for('inicio_privado'))
            else:
                # Credenciales incorrectas o usuario no existe
                flash("Usuario o contraseña incorrecta", 'danger')
                return redirect(url_for('iniciar_sesion'))
                
        except Exception as e:
            # Manejar errores de base de datos u otros errores inesperados
            flash(f"Error al iniciar sesión: {e}", 'danger')
            return redirect(url_for('iniciar_sesion'))
    
    # Si es una petición GET, mostrar el formulario de login
    return render_template('login.html')

# Ruta para cerrar sesión del usuario
@app.route('/cerrar-sesion')
def cerrar_sesion():
    """
    Maneja el cierre de sesión del usuario.
    
    Acciones:
    1. Limpia todas las variables de sesión
    2. Muestra mensaje de confirmación
    3. Redirige al login
    
    Returns:
        Redirect: Redirige a la página de inicio de sesión
    """
    # Limpiar todas las variables de sesión (equivalente a "cerrar sesión")
    session.clear()
    
    # Notificar al usuario que la sesión se cerró correctamente
    flash('Has cerrado sesión correctamente', 'info')
    
    # Redirigir a la página de login
    return redirect(url_for('iniciar_sesion'))

# ============================================================================
# RUTAS PRINCIPALES DE NAVEGACIÓN
# ============================================================================

@app.route('/')
def inicio():
    """
    Ruta principal de la aplicación (página de inicio).
    
    Lógica de enrutamiento:
    - Si el usuario ya tiene sesión activa: redirige al área privada
    - Si no tiene sesión: muestra la página pública con información general
    
    Returns:
        Si hay sesión: Redirect a inicio_privado
        Si no hay sesión: Renderiza index.html con datos de ejemplo
        
    Template Variables:
        proyectos_destacados (list): Lista de proyectos para mostrar en homepage
        noticias_recientes (list): Lista de noticias recientes
        testimonios (list): Lista de testimonios de la comunidad
    """
    # Verificar si el usuario ya está autenticado
    if 'user_id' in session:
        # Si ya tiene sesión, redirigir al área privada
        return redirect(url_for('inicio_privado'))
    
    # Datos de ejemplo para la página pública
    # En un entorno de producción, estos datos vendrían de la base de datos
    proyectos_destacados = [
        {
            'id': 1,
            'titulo': 'Proyecto Educativo Comunitario',
            'descripcion': 'Implementación de programas educativos en comunidades indígenas.',
            'estado': 'en_progreso',
            'estado_color': 'primary',  # Color Bootstrap para el badge de estado
            'imagen': url_for('static', filename='images/pais.jpg')
        },
        {
            'id': 2,
            'titulo': 'Conservación Ambiental',
            'descripcion': 'Proyectos de conservación de la biodiversidad local.',
            'estado': 'completado',
            'estado_color': 'success',
            'imagen': url_for('static', filename='images/ciud.jpg')
        },
        {
            'id': 3,
            'titulo': 'Desarrollo Comunitario',
            'descripcion': 'Iniciativas para el desarrollo sostenible de la comunidad.',
            'estado': 'pendiente',
            'estado_color': 'warning',
            'imagen': url_for('static', filename='images/nue.jpg')
        }
    ]
    
    noticias_recientes = [
        {
            'id': 1,
            'titulo': 'Nuevo programa educativo en comunidades indígenas',
            'contenido': 'Se ha lanzado un nuevo programa educativo que beneficiará a más de 500 niños de comunidades indígenas.',
            'fecha_publicacion': datetime.now() - timedelta(days=5),
            'imagen': url_for('static', filename='images/sinamu.jpg')
        },
        {
            'id': 2,
            'titulo': 'Taller de preservación cultural',
            'contenido': 'Se realizó con éxito el taller de preservación cultural en la comunidad.',
            'fecha_publicacion': datetime.now() - timedelta(days=10),
            'imagen': url_for('static', filename='images/pais.jpg')
        },
        {
            'id': 3,
            'titulo': 'Alianza estratégica con organización internacional',
            'contenido': 'Firmamos una alianza con una organización internacional para promover el desarrollo sostenible.',
            'fecha_publicacion': datetime.now() - timedelta(days=15),
            'imagen': url_for('static', filename='images/ciud.jpg')
        }
    ]
    
    testimonios = [
        {
            'nombre': 'María González',
            'comunidad': 'Comunidad Indígena',
            'mensaje': 'Este proyecto ha transformado positivamente nuestra comunidad.',
            'foto': None  # Sin foto por ahora
        },
        {
            'nombre': 'Carlos Mendoza',
            'comunidad': 'Comunidad Local',
            'mensaje': 'Gracias al apoyo recibido, hemos podido preservar nuestras tradiciones.',
            'foto': None  # Sin foto por ahora
        }
    ]
    
    # Renderizar la página de inicio con todos los datos
    return render_template('index.html', 
                         proyectos_destacados=proyectos_destacados,
                         noticias_recientes=noticias_recientes,
                         testimonios=testimonios)

# ============================================================================
# RUTAS DE REGISTRO Y CONTACTO
# ============================================================================

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """
    Maneja el registro de nuevos usuarios usando FlaskForm.
    
    GET: Muestra el formulario de registro
    POST: Procesa el formulario y crea el usuario
    
    Returns:
        GET: Renderiza registro.html con el formulario
        POST: Redirige a login si es exitoso, o recarga el formulario con errores
    """
    form = RegistroForm()
    
    if form.validate_on_submit():
        # Obtener datos del formulario validado
        nombre = form.nombre.data
        correo = form.correo.data
        contraseña = form.contraseña.data
        imagen = form.imagen.data  # Archivo de imagen (opcional)
        
        # Verificar que el usuario no exista
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuario WHERE correo = %s", (correo,))
            usuario_existente = cur.fetchone()
            
            if usuario_existente:
                flash('El correo ingresado ya se encuentra en uso', 'danger')
                cur.close()
                conn.close()
                return render_template('registro.html', form=form)
            
            # Manejar la subida de imagen de perfil
            imagen_filename = None
            if imagen and imagen.filename:
                # Generar un nombre de archivo seguro
                imagen_filename = secure_filename(imagen.filename)
                # Guardar la imagen en la carpeta de uploads
                imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))
            
            # Encriptar la contraseña antes de guardarla
            hashed_password = generate_password_hash(contraseña)
            
            # Insertar el nuevo usuario en la tabla 'usuario'
            cur.execute("INSERT INTO usuario (nombre, correo, contraseña, imagen) VALUES (%s, %s, %s, %s)",
                        (nombre, correo, hashed_password, imagen_filename))
            conn.commit()  # Guardar cambios
            
            # Cerrar conexión
            cur.close()
            conn.close()
            
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('iniciar_sesion'))
        
        except Exception as e:
            flash(f'Error al registrar usuario: {e}', 'danger')
            return render_template('registro.html', form=form)
    
    # Si es GET o el formulario no es válido, mostrar el formulario
    return render_template('registro.html', form=form)

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    """
    Maneja la página de contacto y procesamiento de mensajes.
    
    GET: Muestra el formulario de contacto
    POST: Procesa el mensaje enviado por el usuario
    
    Form Data (POST):
        nombre (str): Nombre del remitente
        email (str): Correo electrónico del remitente  
        mensaje (str): Contenido del mensaje
        
    Returns:
        GET: Renderiza contacto.html
        POST: Redirect a la misma página con mensaje de confirmación
        
    Note: Actualmente solo muestra un mensaje de confirmación.
          En producción debería guardar en BD o enviar email.
    """
    if request.method == 'POST':
        # Obtener datos del formulario de contacto
        nombre = request.form['nombre']
        email = request.form['email']
        mensaje = request.form['mensaje']
        
        # TODO: Aquí se podría guardar en base de datos o enviar email
        # Por ahora solo mostramos mensaje de confirmación
        flash('¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.', 'success')
        return redirect(url_for('contacto'))
    
    # Si es GET, mostrar el formulario de contacto
    return render_template('contacto.html')

# ============================================================================
# RUTAS DEL ÁREA PRIVADA (REQUIEREN AUTENTICACIÓN)
# ============================================================================

@app.route('/sigic')
@login_required
def inicio_privado():
    """
    Panel principal del área privada para usuarios autenticados.
    
    Muestra:
    - Dashboard con actividades recientes del usuario
    - Resumen de información del sistema
    
    Returns:
        Template: Renderiza inicio_privado.html con datos de actividades
        
    Template Variables:
        actividades (list): Lista de actividades recientes del sistema
        
    Session Requirements:
        - user_id: ID del usuario autenticado
        - user_name: Nombre del usuario
    """
    # Generar actividades recientes (datos de ejemplo)
    # En producción, estos datos vendrían de una tabla de auditoría en la BD
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
    
    # Asegurar compatibilidad con plantillas que usan 'usuario' en lugar de 'user_name'
    session['usuario'] = session.get('user_name', 'Usuario')
    
    return render_template('inicio_privado.html', actividades=actividades)

# ============================================================================
# RUTAS DE INFORMACIÓN INSTITUCIONAL (REQUIEREN AUTENTICACIÓN)
# ============================================================================

@app.route('/sobre-nosotros')
@login_required
def sobre_nosotros():
    """Página con información sobre la organización."""
    return render_template('sobre_nosotros.html')

@app.route('/equipo')
@login_required
def equipo():
    """Página con información del equipo de trabajo."""
    return render_template('equipo.html')

@app.route('/territorio')
@login_required
def territorio():
    """Página con información sobre el territorio y geografía."""
    return render_template('territorio.html')

@app.route('/cosmovision')
@login_required
def cosmovision():
    """Página sobre la cosmovisión y filosofía de las comunidades."""
    return render_template('cosmovision.html')

@app.route('/objetivos')
@login_required
def objetivos():
    """Página con los objetivos estratégicos de la organización."""
    return render_template('objetivos.html')

@app.route('/mision')
@login_required
def mision():
    """Página con la misión de la organización."""
    return render_template('mision.html')

@app.route('/identidad')
@login_required
def identidad():
    """Página sobre la identidad cultural de las comunidades."""
    return render_template('identidad.html')

@app.route('/mision-espiritual')
@login_required
def mision_espiritual():
    """Página sobre la misión espiritual y valores."""
    return render_template('mision_espiritual.html')

@app.route('/modulo')
@login_required
def modulo():
    """Página del módulo educativo o de capacitación."""
    return render_template('modulo.html')

@app.route('/historia')
@login_required
def historia():
    """Página con la historia de la organización."""
    return render_template('historia.html')

@app.route('/proyectos')
def proyectos():
    """
    Lista todos los proyectos del sistema.
    
    Note: No requiere autenticación - es una página pública.
          En producción debería cargar proyectos reales desde la BD.
    
    Returns:
        Template: Renderiza proyectos.html
    """
    return render_template('proyectos.html')

@app.route('/proyecto/<int:id>')
def ver_proyecto(id):
    """
    Muestra los detalles de un proyecto específico.
    
    Args:
        id (int): ID único del proyecto a mostrar
        
    Returns:
        Template: Renderiza ver_proyecto.html con datos del proyecto
        
    Template Variables:
        proyecto (dict): Diccionario con datos del proyecto
        
    Note: Actualmente usa datos de ejemplo. En producción debería:
          1. Consultar la BD para obtener el proyecto por ID
          2. Manejar caso donde el proyecto no existe (404)
    """
    # Datos de ejemplo - en producción esto vendría de la base de datos
    proyecto = {
        'id': id,
        'titulo': 'Proyecto de ejemplo',
        'descripcion': 'Descripción del proyecto',
        # Agregar más campos según la estructura de la BD
    }
    return render_template('ver_proyecto.html', proyecto=proyecto)

# ============================================================================
# RUTAS DE GESTIÓN DE NOTICIAS
# ============================================================================

@app.route('/noticias')
def noticias():
    """
    Lista todas las noticias del sistema.
    
    Note: Página pública que no requiere autenticación.
          En producción debería cargar noticias reales desde la BD.
    
    Returns:
        Template: Renderiza noticias.html
    """
    return render_template('noticias.html')

@app.route('/noticia/<int:id>')
def ver_noticia(id):
    """
    Muestra los detalles de una noticia específica.
    
    Args:
        id (int): ID único de la noticia a mostrar
        
    Returns:
        Template: Renderiza ver_noticia.html con datos de la noticia
        
    Template Variables:
        noticia (dict): Diccionario con datos de la noticia
        
    Note: Usa datos de ejemplo. En producción debería consultar BD.
    """
    # Datos de ejemplo - en producción vendría de la base de datos
    noticia = {
        'id': id,
        'titulo': 'Noticia de ejemplo',
        'contenido': 'Contenido de la noticia',
        # Agregar más campos: fecha, autor, imagen, etc.
    }
    return render_template('ver_noticia.html', noticia=noticia)

# ============================================================================
# RUTAS DE GESTIÓN DE USUARIOS Y PERFILES
# ============================================================================

@app.route('/perfil')
@login_required
def perfil():
    """
    Muestra el perfil del usuario autenticado.
    
    Returns:
        Template: Renderiza perfil.html
        
    Note: Debería cargar datos del usuario desde la BD usando session['user_id']
    """
    return render_template('perfil.html')

@app.route('/editar-perfil')
@login_required
def editar_perfil():
    """
    Formulario para editar el perfil del usuario.
    
    Returns:
        Template: Renderiza editar_perfil.html
        
    Note: Debería soportar POST para guardar cambios en la BD
    """
    return render_template('editar_perfil.html')

# ============================================================================
# RUTAS DE ADMINISTRACIÓN DE CONTENIDO (REQUIEREN AUTENTICACIÓN)
# ============================================================================

@app.route('/agregar-proyecto')
@login_required
def agregar_proyecto():
    """
    Formulario para crear un nuevo proyecto.
    
    Returns:
        Template: Renderiza agregar_proyecto.html
        
    Note: Solo muestra el formulario. Debería tener método POST
          para procesar la creación del proyecto.
    """
    return render_template('agregar_proyecto.html')

@app.route('/editar-proyecto/<int:id>')
@login_required
def editar_proyecto(id):
    """
    Formulario para editar un proyecto existente.
    
    Args:
        id (int): ID del proyecto a editar
        
    Returns:
        Template: Renderiza editar_proyecto.html
        
    Note: Debería cargar datos del proyecto y permitir POST para guardar cambios.
    """
    return render_template('editar_proyecto.html')

@app.route('/agregar-noticia')
@login_required
def agregar_noticia():
    """
    Formulario para crear una nueva noticia.
    
    Returns:
        Template: Renderiza agregar_noticia.html
        
    Note: Debería soportar POST para guardar la noticia en BD
    """
    return render_template('agregar_noticia.html')

@app.route('/editar-noticia/<int:id>')
@login_required
def editar_noticia(id):
    """
    Formulario para editar una noticia existente.
    
    Args:
        id (int): ID de la noticia a editar
        
    Returns:
        Template: Renderiza editar_noticia.html
        
    Note: Debería cargar datos de la noticia y soportar POST para guardar cambios
    """
    return render_template('editar_noticia.html')

# ============================================================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# ============================================================================

if __name__ == '__main__':
    """
    Punto de entrada principal de la aplicación Flask.
    
    Configuración de desarrollo:
    - host='0.0.0.0': Permite conexiones desde cualquier IP (útil para desarrollo)
    - port=5000: Puerto estándar de Flask
    - debug=True: Modo debug activado (auto-reload, mensajes de error detallados)
    
    IMPORTANTE: En producción cambiar debug=False y usar un servidor WSGI como Gunicorn
    """
    app.run(host='0.0.0.0', port=5000, debug=True)