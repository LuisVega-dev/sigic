# ============================================================================
# IMPORTACIONES - Librerías necesarias para la aplicación Flask
# ============================================================================
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from .database import get_db_connection  # Para conexión a MySQL
from .config import Config  # Para configuración de la aplicación
from flask import jsonify  # Para respuestas JSON en API
import os  # Para operaciones del sistema de archivos
from werkzeug.utils import secure_filename  # Para nombres de archivo seguros
from werkzeug.security import generate_password_hash, check_password_hash  # Para encriptación de contraseñas
from functools import wraps  # Para crear decoradores
from itsdangerous import URLSafeSerializer  # Para encriptación segura de URLs

# ============================================================================
# CONFIGURACIÓN DEL BLUEPRINT
# ============================================================================
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ============================================================================
# FUNCIONES AUXILIARES Y DECORADORES
# ============================================================================

# Funciones para encriptación segura de IDs en URLs
def get_serializer():
    """
    Retorna un serializador seguro usando la clave secreta de la aplicación.
    """
    return URLSafeSerializer(Config.SECRET_KEY)

def encrypt_id(id):
    """
    Encripta un ID de forma segura para usar en URLs.
    Args:
        id (int): ID a encriptar
    Returns:
        str: Token encriptado seguro para URLs
    """
    s = get_serializer()
    return s.dumps(id)

def decrypt_id(token):
    """
    Desencripta un token y retorna el ID original.
    Args:
        token (str): Token encriptado
    Returns:
        int: ID original o None si el token es inválido
    """
    s = get_serializer()
    try:
        return s.loads(token)
    except:
        return None

# Decorador para proteger las rutas que requieren inicio de sesión
def login_required(f):
    """
    Decorador que verifica si el usuario ha iniciado sesión.
    Si no hay sesión activa, redirige al login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si existe una sesión de administrador activa
        if 'admin_id' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# RUTAS DE AUTENTICACIÓN Y SESIÓN
# ============================================================================

# Login - Ruta para el inicio de sesión de administradores
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
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
            admin = cur.fetchone()
            
            # Cerrar la conexión a la base de datos
            cur.close()
            conn.close()
            
            # Verificar si el usuario existe
            if admin:
                # Verificar si el usuario tiene permisos de administrador
                if not admin.get('admin'):
                    flash("El usuario no es administrador", 'danger')
                    return redirect(url_for('admin.login'))
                
                # Verificar la contraseña usando hash
                if check_password_hash(admin['contraseña'], password):
                    # Crear la sesión del administrador
                    session['admin_id'] = admin['id']
                    session['admin_name'] = admin['nombre']
                    session['admin_image'] = admin.get('imagen')  # Guardar la imagen en sesión
                    
                    return redirect(url_for('admin.index'))
                else:
                    # Contraseña incorrecta
                    flash("Credenciales incorrectas", 'danger')
                    return redirect(url_for('admin.login'))
            else:
                # Usuario no encontrado
                flash("Usuario no registrado", 'warning')
                return redirect(url_for('admin.login'))
                
        except Exception as e:
            # Manejar errores de base de datos u otros errores
            flash(f"Error al iniciar sesión: {e}", 'danger')
            return redirect(url_for('admin.login'))
    
    # Si es una petición GET, mostrar el formulario de login
    return render_template('admin/login.html')

# ============================================================================

# Ruta para cerrar sesión
@admin_bp.route('/logout')
def logout():
    """
    Función para cerrar la sesión del administrador.
    Limpia todos los datos de sesión y redirige al login.
    """
    # Limpiar todos los datos de la sesión
    session.clear()
    return redirect(url_for('admin.login'))

# ============================================================================
# RUTAS DE GESTIÓN DE USUARIOS
# ============================================================================

# Ruta para la página de inicio: Mostrar todos los usuarios
@admin_bp.route('/')
@login_required  # Asegura que solo los administradores puedan acceder
def index():
    """
    Página principal que muestra la lista de todos los usuarios registrados.
    """
    try:
        # Conectar a la base de datos
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Obtener todos los usuarios excepto el administrador actual
        # Esto evita que el administrador se muestre a sí mismo en la lista
        cur.execute("SELECT * FROM usuario WHERE id != %s", (session.get('admin_id'),)) 
        data = cur.fetchall()
        
        # Cerrar conexión
        cur.close()
        conn.close()
        
        # Renderizar la plantilla con los datos de usuarios
        return render_template('admin/index.html', usuarios=data)
    except Exception as e:
        # En caso de error, mostrar página con mensaje de error
        flash(f"Error al obtener datos: {e}", "danger")
        return render_template('admin/index.html', usuarios=[], message=f"Error al obtener datos: {e}", message_type="danger")

# Ruta para agregar un nuevo usuario
@admin_bp.route('/add', methods=['GET','POST'])
@login_required  # Asegura que solo los administradores puedan acceder
def add_user():
    """
    Función para agregar un nuevo usuario al sistema.
    GET: Muestra el formulario de registro
    POST: Procesa los datos y crea el usuario
    """
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        correo = request.form['correo']
        password = request.form['contraseña']
        imagen = request.files['imagen']
        
        # Encriptar la contraseña antes de guardarla (seguridad)
        hashed_password = generate_password_hash(password)
        
        # Manejar la subida de imagen de perfil
        imagen_filename = None
        
        if imagen and imagen.filename:
            # Generar un nombre de archivo seguro
            imagen_filename = secure_filename(imagen.filename)
            # Guardar la imagen en la carpeta de uploads
            imagen.save(os.path.join(Config.UPLOAD_FOLDER, imagen_filename))

        # Verificar si se subió una imagen válida
        if imagen and imagen.filename:
            # Generar un nombre de archivo seguro
            imagen_filename = secure_filename(imagen.filename)
            # Guardar la imagen en la carpeta de uploads
            imagen.save(os.path.join(Config.UPLOAD_FOLDER, imagen_filename))

        try:
            # Conectar a la base de datos
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Insertar el nuevo usuario en la base de datos
            cur.execute(
                "INSERT INTO usuario (nombre, correo, contraseña, imagen) VALUES (%s, %s, %s, %s)",
                (nombre, correo, hashed_password, imagen_filename)
            )
            
            # Confirmar los cambios
            conn.commit()
            cur.close()
            conn.close()
            
            flash("Usuario agregado correctamente", 'success')
            return redirect(url_for('admin.index'))
        except Exception as e:
            # Manejar errores de base de datos
            flash(f"Error al agregar usuario: {e}", 'danger')
            return redirect(url_for('admin.index'))
    
    # Si es GET, mostrar el formulario
    return render_template('admin/agregar.html')

# Ruta para editar un usuario existente
@admin_bp.route('/edit/<token>', methods=['GET','POST'])
@login_required  # Asegura que solo los administradores puedan acceder
def edit_user(token):
    """
    Función para editar un usuario existente usando token encriptado.
    GET: Muestra el formulario prellenado con los datos actuales
    POST: Actualiza los datos del usuario
    """
    # Desencriptar el token para obtener el ID real
    id = decrypt_id(token)
    if id is None:
        flash("Token inválido", 'danger')
        return redirect(url_for('admin.index'))
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if request.method == 'POST':
            # Obtener los nuevos datos del formulario
            nombre = request.form['nombre']
            correo = request.form['correo']
            password = request.form['contraseña']
            
            # Manejar la imagen (opcional)
            imagen = request.files.get('imagen')
            
            # Obtener los datos actuales del usuario para preservar valores no modificados
            cur.execute("SELECT imagen, contraseña FROM usuario WHERE id=%s", (id,))
            usuario_actual = cur.fetchone()
            imagen_filename = usuario_actual['imagen'] if usuario_actual else None
            hashed_password = usuario_actual['contraseña'] if usuario_actual else None
            
            # Si se sube una nueva imagen, procesarla
            if imagen and imagen.filename:
                imagen_filename = secure_filename(imagen.filename)
                imagen.save(os.path.join(current_app.config['UPLOAD_FOLDER'], imagen_filename))
            
            # Si se proporciona una nueva contraseña, encriptarla
            if password:
                hashed_password = generate_password_hash(password)
            
            # Actualizar el usuario en la base de datos
            cur.execute(
                "UPDATE usuario SET nombre=%s, correo=%s, contraseña=%s, imagen=%s WHERE id=%s",
                (nombre, correo, hashed_password, imagen_filename, id)
            )
            conn.commit()
            cur.close()
            conn.close()
            
            flash("Usuario actualizado correctamente", 'success')
            return redirect(url_for('admin.index'))
        else:
            # GET: Obtener los datos actuales del usuario para mostrar en el formulario
            cur.execute("SELECT * FROM usuario WHERE id=%s", (id,))
            usuario = cur.fetchone()
            cur.close()
            conn.close()
            return render_template('admin/editar.html', usuario=usuario)
    except Exception as e:
        flash(f"Error al editar usuario: {e}", 'error')
        return redirect(url_for('admin.index'))
    
# Ruta para eliminar un usuario
@admin_bp.route('/delete/<token>', methods=['GET','POST'])
@login_required  # Asegura que solo los administradores puedan acceder
def delete_user(token):
    """
    Función para eliminar un usuario del sistema usando token encriptado.
    Elimina permanentemente el registro de la base de datos.
    """
    # Desencriptar el token para obtener el ID real
    id = decrypt_id(token)
    if id is None:
        flash("Token inválido", 'error')
        return redirect(url_for('admin.index'))
    
    try:
        # Conectar a la base de datos
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Eliminar el usuario por su ID
        cur.execute("DELETE FROM usuario WHERE id=%s", (id,))
        conn.commit()
        
        # Cerrar conexión
        cur.close()
        conn.close()
        
        flash("Usuario eliminado correctamente", 'success')
    except Exception as e:
        # Manejar errores durante la eliminación
        flash(f"Error al eliminar usuario: {e}", 'error')
    
    return redirect(url_for('admin.index'))

# ============================================================================
# RUTAS DE GESTIÓN DE ADMINISTRADORES
# ============================================================================

# Ruta para promover un usuario a administrador
@admin_bp.route('/add_admin/<token>', methods=['GET', 'POST'])
@login_required  # Asegura que solo los administradores puedan acceder
def add_admin(token):
    """
    Función para otorgar permisos de administrador a un usuario existente usando token encriptado.
    Verifica que el usuario no sea ya administrador antes de promoverlo.
    """
    # Desencriptar el token para obtener el ID real
    id = decrypt_id(token)
    if id is None:
        flash("Token inválido", 'error')
        return redirect(url_for('admin.index'))
    
    try:
        # Verificar si el usuario ya tiene permisos de administrador
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT admin FROM usuario WHERE id = %s", (id,))
        usuario = cur.fetchone()
        
        # Si ya es administrador, mostrar mensaje informativo
        if usuario and usuario.get('admin'):
            flash("El usuario ya es administrador", 'info')
            cur.close()
            conn.close()
            return redirect(url_for('admin.index'))
        
        cur.close()
        conn.close()

        # Promover el usuario a administrador
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE usuario SET admin = TRUE WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        
        flash("Usuario promovido a administrador", 'success')
    except Exception as e:
        flash(f"Error al promover usuario a administrador: {e}", 'error')
    
    return redirect(url_for('admin.index'))

# Ruta para remover permisos de administrador a un usuario
@admin_bp.route('/remove_admin/<token>', methods=['GET', 'POST'])
@login_required  # Asegura que solo los administradores puedan acceder
def remove_admin(token):
    """
    Función para quitar permisos de administrador a un usuario existente usando token encriptado.
    """
    # Desencriptar el token para obtener el ID real
    id = decrypt_id(token)
    if id is None:
        flash("Token inválido", 'error')
        return redirect(url_for('admin.index'))
    
    try:
        # Conectar a la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Actualizamos el usuario para quitarle los permisos de administrador
        cur.execute("UPDATE usuario SET admin = FALSE WHERE id = %s", (id,))
        conn.commit()

        # Cerrar conexión
        cur.close()
        conn.close()
        
        flash("Permisos de administrador removidos correctamente", 'success')
    except Exception as e:
        flash(f"Error al remover permisos de administrador: {e}", 'error')
    
    return redirect(url_for('admin.index'))

# Ruta para mostrar la lista de administradores
@admin_bp.route('/admins')
@login_required  # Asegura que solo los administradores puedan acceder
def admins():
    """
    Página que muestra la lista de todos los administradores del sistema.
    """
    try:
        # Conectar a la base de datos
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Obtener solo los usuarios que son administradores
        cur.execute("SELECT * FROM usuario WHERE admin = TRUE")
        admins = cur.fetchall()
        
        # Cerrar conexión
        cur.close()
        conn.close()
        
        # Renderizar la plantilla con los datos de administradores
        return render_template('admin/admin_table.html', admins=admins)
    except Exception as e:
        flash(f"Error al obtener administradores: {e}", 'error')
        return render_template('admin/admin_table.html', admins=[], message=f"Error al obtener administradores: {e}", message_type="error")

# ============================================================================
# RUTAS API - Endpoints para acceso programático a los datos
# ============================================================================

# Ruta API para obtener los usuarios
@admin_bp.route('/api/usuarios', methods=['GET'])    
def api_usuarios():
    """
    API endpoint que retorna todos los usuarios en formato JSON.
    Utilizado para integración con aplicaciones externas.
    """
    try:
        # Conectar a la base de datos
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Obtener todos los usuarios
        cur.execute("SELECT * FROM usuario")
        usuarios = cur.fetchall()
        
        # Cerrar conexión
        cur.close()
        conn.close()
        
        # Retornar los datos en formato JSON
        return jsonify(usuarios)
    except Exception as e:
        # Retornar error en formato JSON
        return jsonify({"error": str(e)}), 500

# ============================================================================   
# Modificar Perfil de Administrador
# ============================================================================

# Ruta para editar el perfil del administrador
@admin_bp.route('/edit_profile/<token>', methods=['GET', 'POST'])
@login_required  # Asegura que solo los administradores puedan acceder
def edit_profile(token):
    """
    Función para editar el perfil del administrador usando token encriptado.
    Permite cambiar nombre, correo y contraseña.
    """
    # Desencriptar el token para obtener el ID real
    id = decrypt_id(token)
    if id is None:
        flash("Token inválido", 'danger')
        return redirect(url_for('admin.index'))
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        if request.method == 'POST':
            # Obtener los nuevos datos del formulario
            nombre = request.form['nombre']
            correo = request.form['correo']
            password = request.form['contraseña']
            
            # Manejar la imagen (opcional)
            imagen = request.files.get('imagen')
            imagen_filename = None
            
            # Obtener los datos actuales del administrador para preservar valores no modificados
            cur.execute("SELECT imagen, contraseña FROM usuario WHERE id=%s", (id,))
            admin_actual = cur.fetchone()
            imagen_filename = admin_actual['imagen'] if admin_actual else None
            hashed_password = admin_actual['contraseña'] if admin_actual else None
            
            # Si se sube una nueva imagen, procesarla
            if imagen and imagen.filename:
                imagen_filename = secure_filename(imagen.filename)
                imagen.save(os.path.join(current_app.config['UPLOAD_FOLDER'], imagen_filename))
            
            # Si se proporciona una nueva contraseña, encriptarla
            if password:
                hashed_password = generate_password_hash(password)
            
            # Actualizar el perfil del administrador en la base de datos
            cur.execute(
                "UPDATE usuario SET nombre=%s, correo=%s, contraseña=%s, imagen=%s WHERE id=%s",
                (nombre, correo, hashed_password, imagen_filename, id)
            )
            conn.commit()
            
            # Actualizar los datos de la sesión si el administrador editó su propio perfil
            if id == session.get('admin_id'):
                session['admin_name'] = nombre
                if imagen_filename:
                    session['admin_image'] = imagen_filename
            
            flash("Perfil actualizado correctamente", 'success')
            return redirect(url_for('admin.index'))
        else:
            # GET: Obtener los datos actuales del administrador para mostrar en el formulario
            cur.execute("SELECT * FROM usuario WHERE id=%s", (id,))
            admin = cur.fetchone()
            cur.close()
            conn.close()
            return render_template('admin/edit_profile.html', user_admin=admin)
    except Exception as e:
        flash(f"Error al editar perfil: {e}", 'error')
        return redirect(url_for('admin.index'))


# ============================================================================
# PROCESADORES DE CONTEXTO Y CONFIGURACIÓN FINAL
# ============================================================================

# Filtro personalizado para encriptar IDs en plantillas
@admin_bp.app_template_filter('encrypt_id')
def encrypt_id_filter(id):
    """
    Filtro de Jinja2 para encriptar IDs en las plantillas.
    Uso: {{ usuario.id | encrypt_id }}
    """
    return encrypt_id(id)

# Context processor para inyectar variables en las plantillas
@admin_bp.context_processor
def inject_admin():
    """
    Inyecta datos del administrador en todas las plantillas.
    Permite acceder a admin_name, admin_image y admin_token desde cualquier template.
    """
    admin_id = session.get('admin_id')
    admin_token = encrypt_id(admin_id) if admin_id else None
    
    return {
        'admin_name': session.get('admin_name'),
        'admin_image': session.get('admin_image'),
        'admin_token': admin_token  # Token encriptado para URLs seguras
    }