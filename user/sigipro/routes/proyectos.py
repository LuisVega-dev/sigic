from flask import Blueprint, render_template
from .decorators import login_required

proyectos_bp = Blueprint('proyectos', __name__)

@proyectos_bp.route('/proyectos')
def proyectos():
    """Lista todos los proyectos del sistema."""
    return render_template('proyects/proyectos.html')

@proyectos_bp.route('/proyecto/<int:id>')
def ver_proyecto(id):
    """Muestra los detalles de un proyecto específico."""
    proyecto = {
        'id': id,
        'titulo': 'Proyecto de ejemplo',
        'descripcion': 'Descripción del proyecto',
    }
    return render_template('proyects/ver_proyecto.html', proyecto=proyecto)

@proyectos_bp.route('/agregar-proyecto')
@login_required
def agregar_proyecto():
    """Formulario para crear un nuevo proyecto."""
    return render_template('proyects/agregar_proyecto.html')

@proyectos_bp.route('/editar-proyecto/<int:id>')
@login_required
def editar_proyecto(id):
    """Formulario para editar un proyecto existente."""
    return render_template('proyects/editar_proyecto.html')