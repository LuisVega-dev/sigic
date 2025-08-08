from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os
from .decorators import login_required
from .database import get_db_connection
from .forms import PerfilForm
from .config import Config

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/perfil')
@login_required
def perfil():
    """Muestra el perfil del usuario autenticado."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario WHERE id = %s", (session['user_id'],))
        usuario = cur.fetchone()
        cur.close()
        conn.close()
        
        if not usuario:
            flash('Usuario no encontrado', 'danger')
            return redirect(url_for('main.inicio_privado'))
            
        return render_template('user/perfil.html', usuario=usuario)

    except Exception as e:
        flash(f'Error al cargar perfil: {e}', 'danger')
        return redirect(url_for('main.inicio_privado'))

@usuarios_bp.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    """Formulario para editar el perfil del usuario."""
    form = PerfilForm()
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario WHERE id = %s", (session['user_id'],))
        usuario = cur.fetchone()
        cur.close()
        conn.close()
        
        if not usuario:
            flash('Usuario no encontrado', 'danger')
            return redirect(url_for('usuarios.perfil'))
            
    except Exception as e:
        flash(f'Error al cargar datos del usuario: {e}', 'danger')
        return redirect(url_for('usuarios.perfil'))
    
    if form.validate_on_submit():
        nombre_completo = form.nombre_completo.data
        email = form.email.data
        foto_perfil = form.foto_perfil.data
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuario WHERE correo = %s AND id != %s", (email, session['user_id']))
            email_existente = cur.fetchone()
            
            if email_existente:
                flash('El correo ingresado ya está siendo usado por otro usuario', 'danger')
                cur.close()
                conn.close()
                return render_template('user/editar_perfil.html', form=form, usuario=usuario)
            
            foto_filename = usuario.get('imagen')
            if foto_perfil and foto_perfil.filename:
                foto_filename = secure_filename(foto_perfil.filename)
                foto_perfil.save(os.path.join(Config.UPLOAD_FOLDER, foto_filename))
            
            cur.execute("""
                UPDATE usuario 
                SET nombre = %s, correo = %s, imagen = %s
                WHERE id = %s
            """, (nombre_completo, email, foto_filename, session['user_id']))
            
            conn.commit()
            cur.close()
            conn.close()
            
            session['user_name'] = nombre_completo
            session['usuario'] = nombre_completo
            
            flash('Perfil actualizado exitosamente', 'success')
            return redirect(url_for('usuarios.perfil'))
            
        except Exception as e:
            flash(f'Error al actualizar perfil: {e}', 'danger')
            return render_template('user/editar_perfil.html', form=form, usuario=usuario)
    
    if request.method == 'GET':
        form.nombre_completo.data = usuario.get('nombre', '')
        form.email.data = usuario.get('correo', '')
        form.telefono.data = usuario.get('telefono', '')
        form.direccion.data = usuario.get('direccion', '')
        form.biografia.data = usuario.get('biografia', '')

    return render_template('user/editar_perfil.html', form=form, usuario=usuario)