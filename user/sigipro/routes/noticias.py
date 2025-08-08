from flask import Blueprint, render_template
from .decorators import login_required

noticias_bp = Blueprint('noticias', __name__)

@noticias_bp.route('/noticias')
def noticias():
    """Lista todas las noticias del sistema."""
    return render_template('noticias/noticias.html')

@noticias_bp.route('/noticia/<int:id>')
def ver_noticia(id):
    """Muestra los detalles de una noticia específica."""
    noticia = {
        'id': id,
        'titulo': 'Noticia de ejemplo',
        'contenido': 'Contenido de la noticia',
    }
    return render_template('noticias/ver_noticia.html', noticia=noticia)

@noticias_bp.route('/agregar-noticia')
@login_required
def agregar_noticia():
    """Formulario para crear una nueva noticia."""
    return render_template('noticias/agregar_noticia.html')

@noticias_bp.route('/editar-noticia/<int:id>')
@login_required
def editar_noticia(id):
    """Formulario para editar una noticia existente."""
    return render_template('noticias/editar_noticia.html')