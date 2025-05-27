from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
CORS(app, origins=["http://localhost:3000", "http://192.168.1.1"])
app.secret_key = 'secretkey'

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
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO usuario (nombre, correo, contraseña) VALUES (%s, %s, %s)", (nombre, correo, password))
            conn.commit()
            cur.close()
            conn.close()
            # Usar flash antes de redirigir
            return redirect(url_for('index'), message="Usuario agregado correctamente", message_type="success")
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
            cur.execute("UPDATE usuario SET nombre=%s, correo=%s, contraseña=%s WHERE id=%s", (nombre, correo, password, id))
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
    
# Ejecutamos la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)