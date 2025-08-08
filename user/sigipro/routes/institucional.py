from flask import Blueprint, render_template
from .decorators import login_required

institucional_bp = Blueprint('institucional', __name__)

@institucional_bp.route('/sobre-nosotros')
@login_required
def sobre_nosotros():
    """Página con información sobre la organización."""
    return render_template('institucional/sobre_nosotros.html')

@institucional_bp.route('/equipo')
@login_required
def equipo():
    """Página con información del equipo de trabajo."""
    return render_template('institucional/equipo.html')

@institucional_bp.route('/comunidad')
@login_required
def comunidad():
    """Página con información sobre la comunidad."""
    return render_template('institucional/comunidad.html')

@institucional_bp.route('/territorio')
@login_required
def territorio():
    """Página con información sobre el territorio y geografía."""
    return render_template('institucional/territorio.html')

@institucional_bp.route('/cosmovision')
@login_required
def cosmovision():
    """Página sobre la cosmovisión y filosofía de las comunidades."""
    return render_template('institucional/cosmovision.html')

@institucional_bp.route('/objetivos')
@login_required
def objetivos():
    """Página con los objetivos estratégicos de la organización."""
    return render_template('institucional/objetivos.html')

@institucional_bp.route('/mision')
@login_required
def mision():
    """Página con la misión de la organización."""
    return render_template('institucional/mision.html')

@institucional_bp.route('/identidad')
@login_required
def identidad():
    """Página sobre la identidad cultural de las comunidades."""
    return render_template('institucional/identidad.html')

@institucional_bp.route('/mision-espiritual')
@login_required
def mision_espiritual():
    """Página sobre la misión espiritual y valores."""
    return render_template('institucional/mision_espiritual.html')

@institucional_bp.route('/modulo')
@login_required
def modulo():
    """Página del módulo educativo o de capacitación."""
    return render_template('institucional/modulo.html')

@institucional_bp.route('/historia')
@login_required
def historia():
    """Página con la historia de la organización."""
    return render_template('institucional/historia.html')