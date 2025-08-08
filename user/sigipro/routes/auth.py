from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from .database import get_db_connection
from .forms import RegistroForm
from .config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/iniciar-sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    """Maneja el proceso de inicio de sesión de usuarios."""
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['contraseña']
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuario WHERE correo=%s", (correo,))
            user = cur.fetchone()
            cur.close()
            conn.close()
            
            if user and check_password_hash(user['contraseña'], password):
                session['user_id'] = user['id']
                session['user_name'] = user['nombre']
                session['usuario'] = user['nombre']
                session['user_image'] = user.get('imagen')
                session['user_admin'] = user.get('admin', False)
                
                flash("Inicio de sesión exitoso", 'success')
                return redirect(url_for('main.inicio_privado'))
            else:
                flash("Usuario o contraseña incorrecta", 'danger')
                return redirect(url_for('auth.iniciar_sesion'))
                
        except Exception as e:
            flash(f"Error al iniciar sesión: {e}", 'danger')
            return redirect(url_for('auth.iniciar_sesion'))
    
    return render_template('auth/login.html')

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """Maneja el registro de nuevos usuarios usando FlaskForm."""
    form = RegistroForm()
    
    if form.validate_on_submit():
        nombre = form.nombre.data
        correo = form.correo.data
        contraseña = form.contraseña.data
        imagen = form.imagen.data
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuario WHERE correo = %s", (correo,))
            usuario_existente = cur.fetchone()
            
            if usuario_existente:
                flash('El correo ingresado ya se encuentra en uso', 'danger')
                cur.close()
                conn.close()
                return render_template('auth/registro.html', form=form)
            
            imagen_filename = None
            if imagen and imagen.filename:
                imagen_filename = secure_filename(imagen.filename)
                imagen.save(os.path.join(Config.UPLOAD_FOLDER, imagen_filename))
            
            hashed_password = generate_password_hash(contraseña)
            
            cur.execute("INSERT INTO usuario (nombre, correo, contraseña, imagen) VALUES (%s, %s, %s, %s)",
                        (nombre, correo, hashed_password, imagen_filename))
            conn.commit()
            cur.close()
            conn.close()
            
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.iniciar_sesion'))
        
        except Exception as e:
            flash(f'Error al registrar usuario: {e}', 'danger')
            return render_template('auth/registro.html', form=form)
    
    return render_template('auth/registro.html', form=form)

@auth_bp.route('/cerrar-sesion')
def cerrar_sesion():
    """Maneja el cierre de sesión del usuario."""
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('main.inicio'))