from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql
from flask import jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
CORS(app)
CORS(app, origins=["http://localhost:5173/", "http://192.168.10.1"])
app.secret_key = 'secretkey'
UPLOAD_FOLDER = 'static/uploads_image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Decorador para proteger las rutas que requieren inicio de sesión
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        charset='utf8mb4',
        use_unicode=True,
        database='sigic',
        cursorclass=pymysql.cursors.DictCursor,
    )

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['contraseña']
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM editor WHERE correo=%s", (correo,))
            admin = cur.fetchone()
            cur.close()
            conn.close()
            if admin and check_password_hash(admin['contraseña'], password):
                session['admin_id'] = admin['id']
                session['admin_name'] = admin['nombre']
                session['admin_image'] = admin.get('imagen')  # Guarda la imagen en sesión
                flash("Login exitoso", 'success')
                return redirect(url_for('index'))
            else:
                flash("Credenciales incorrectas", 'danger')
                return redirect(url_for('login'))
        except Exception as e:
            flash(f"Error al iniciar sesión: {e}", 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

# Ruta para la pagina de inicio: Mostrar todos los usuarios
@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html', usuarios=data)
    except Exception as e:
        flash(f"Error al obtener datos: {e}")
        return render_template('index.html', usuarios=[], message=f"Error al obtener datos: {e}", message_type="error")

# Ruta para agregar un nuevo usuario
@app.route('/add', methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        password = request.form['contraseña']
        # Encriptar la contraseña antes de guardarla
        hashed_password = generate_password_hash(password)
        # Obtener la imagen del formulario
        imagen = request.files['imagen']
        # Verificar si se subió una imagen
        imagen_filename = None
        if imagen and imagen.filename:
            imagen_filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO usuario (nombre, correo, contraseña, imagen) VALUES (%s, %s, %s, %s)",
                (nombre, correo, hashed_password, imagen_filename)
            )
            conn.commit()
            cur.close()
            conn.close()
            flash("Usuario agregado correctamente", 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error al agregar usuario: {e}", 'error')
            return redirect(url_for('index'))
    return render_template('agregar.html')

# Ruta para editar un usuario existente
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_user(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        if request.method == 'POST':
            nombre = request.form['nombre']
            correo = request.form['correo']
            password = request.form['contraseña']
            # Encriptar la contraseña antes de guardarla
            hashed_password = generate_password_hash(password)
            # Obtener la imagen del formulario
            imagen = request.files.get('imagen')
            # Obtener el nombre de la imagen actual
            cur.execute("SELECT imagen FROM usuario WHERE id=%s", (id,))
            usuario_actual = cur.fetchone()
            imagen_filename = usuario_actual['imagen'] if usuario_actual else None
            # Si se sube una nueva imagen, la guardamos y actualizamos el nombre
            if imagen and imagen.filename:
                from werkzeug.utils import secure_filename
                import os
                imagen_filename = secure_filename(imagen.filename)
                imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))
            cur.execute(
                "UPDATE usuario SET nombre=%s, correo=%s, contraseña=%s, imagen=%s WHERE id=%s",
                (nombre, correo, hashed_password, imagen_filename, id)
            )
            conn.commit()
            cur.close()
            conn.close()
            flash("Usuario actualizado correctamente", 'success')
            return redirect(url_for('index'))
        else:
            cur.execute("SELECT * FROM usuario WHERE id=%s", (id,))
            usuario = cur.fetchone()
            cur.close()
            conn.close()
            return render_template('editar.html', usuario=usuario)
    except Exception as e:
        flash(f"Error al editar usuario: {e}", 'error')
        return redirect(url_for('index'))
    
# Ruta para eliminar un usuario
@app.route('/delete/<int:id>', methods=['GET','POST'])
def delete_user(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM usuario WHERE id=%s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        flash("Usuario eliminado correctamente", 'success')
    except Exception as e:
        flash(f"Error al eliminar usuario: {e}", 'error')
    return redirect(url_for('index'))

#----------------------------Editores--------------------------------

#Ruta para agregar un editor
@app.route('/add_editor', methods=['GET','POST'])
def add_editor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        password = request.form['contraseña']
        # Encriptar la contraseña antes de guardarla
        hashed_password = generate_password_hash(password)
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            # Verificar si el correo ya está registrado en la tabla usuario
            cur.execute("SELECT id FROM usuario WHERE correo = %s", (correo,))
            # Verificar si el correo ya está registrado
            id_usuario = cur.fetchone()
            if id_usuario:
                id_usuario = id_usuario['id']
            else:
                flash("El correo no está registrado", 'daneger')
                return redirect(url_for('index'))
            # Insertar el editor en la tabla editor
            cur.execute("INSERT INTO editor (nombre, correo, contraseña, id_usuario) VALUES (%s, %s, %s, %s)", (nombre, correo, hashed_password, id_usuario))
            conn.commit()
            cur.close()
            conn.close()
            flash("Editor agregado correctamente", 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error al agregar editor: {e}", 'error')
            return redirect(url_for('index'))
    return render_template('agregar_editor.html')

#Ruta para la pagina de inicio: Mostrar todos los editores
@app.route('/editors')
def editors():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM editor")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('editors.html', editors=data)
    except Exception as e:
        flash(f"Error al obtener datos: {e}")
        return render_template('editors.html', editors=[], message=f"Error al obtener datos: {e}", message_type="error")    
    
# Ruta para editar un editor existente
@app.route('/edit_editor/<int:id>', methods=['GET','POST'])
def edit_editor(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        if request.method == 'POST':
            nombre = request.form['nombre']
            correo = request.form['correo']
            password = request.form['contraseña']
            # Encriptar la contraseña antes de guardarla
            hashed_password = generate_password_hash(password)
            cur.execute(
                "UPDATE editor SET nombre=%s, correo=%s, contraseña=%s WHERE id=%s",
                (nombre, correo, hashed_password, id)
            )
            conn.commit()
            cur.close()
            conn.close()
            flash("Editor actualizado correctamente", 'success')
            return redirect(url_for('editors'))
        else:
            cur.execute("SELECT * FROM editor WHERE id=%s", (id,))
            editor = cur.fetchone()
            cur.close()
            conn.close()
            return render_template('edit_editor.html', editor=editor)
    except Exception as e:
        flash(f"Error al editar editor: {e}", 'error')
        return redirect(url_for('editors'))
    
# Ruta para eliminar un editor
@app.route('/delete_editor/<int:id>', methods=['GET','POST'])
def delete_editor(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM editor WHERE id=%s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        flash("Editor eliminado correctamente", 'success')
    except Exception as e:
        flash(f"Error al eliminar editor: {e}", 'error')
    return redirect(url_for('editors'))

#RUTAS API

# Ruta API para obtener los usuarios
@app.route('/api/usuarios', methods=['GET'])    
def api_usuarios():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario")
        usuarios = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(usuarios)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta Api para obtener los editores
@app.route('/api/editors', methods=['GET'])
def api_editors():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM editor")
        editors = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(editors)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada", "success")
    return redirect(url_for('login'))

# Context processor para inyectar variables en las plantillas
@app.context_processor
def inject_admin():
    return {
        'admin_name': session.get('admin_name'),
        'admin_image': session.get('admin_image')
    }

# Ejecutamos la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)