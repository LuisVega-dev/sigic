from datetime import datetime, timedelta
from flask import url_for

def get_proyectos_destacados():
    """Retorna proyectos destacados para la página de inicio"""
    return [
        {
            'id': 1,
            'titulo': 'Proyecto Educativo Comunitario',
            'descripcion': 'Implementación de programas educativos en comunidades indígenas.',
            'estado': 'en_progreso',
            'estado_color': 'primary',
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

def get_noticias_recientes():
    """Retorna noticias recientes para la página de inicio"""
    return [
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

def get_testimonios():
    """Retorna testimonios para la página de inicio"""
    return [
        {
            'nombre': 'María González',
            'comunidad': 'Comunidad Indígena',
            'mensaje': 'Este proyecto ha transformado positivamente nuestra comunidad.',
            'foto': None
        },
        {
            'nombre': 'Carlos Mendoza',
            'comunidad': 'Comunidad Local',
            'mensaje': 'Gracias al apoyo recibido, hemos podido preservar nuestras tradiciones.',
            'foto': None
        }
    ]