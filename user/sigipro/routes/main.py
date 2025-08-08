from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta
from .decorators import login_required
from .utils import get_proyectos_destacados, get_noticias_recientes, get_testimonios

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def inicio():
    """Ruta principal de la aplicación (página de inicio)."""
    if 'user_id' in session:
        return redirect(url_for('main.inicio_privado'))
    
    proyectos_destacados = get_proyectos_destacados()
    noticias_recientes = get_noticias_recientes()
    testimonios = get_testimonios()
    
    return render_template('index.html', 
                         proyectos_destacados=proyectos_destacados,
                         noticias_recientes=noticias_recientes,
                         testimonios=testimonios)

@main_bp.route('/contacto', methods=['GET', 'POST'])
def contacto():
    """Maneja la página de contacto y procesamiento de mensajes."""
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        mensaje = request.form['mensaje']
        
        flash('¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.', 'success')
        return redirect(url_for('main.contacto'))
    
    return render_template('contacto.html')

@main_bp.route('/sigic')
@login_required
def inicio_privado():
    """Panel principal del área privada para usuarios autenticados."""
    
    session['usuario'] = session.get('user_name')

    return render_template('inicio_privado.html')