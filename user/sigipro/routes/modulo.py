from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, session, send_file
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename

modulo_bp = Blueprint('modulo', __name__)

# Configuración para subida de archivos
UPLOAD_FOLDER = 'static/uploads/guias'
ALLOWED_EXTENSIONS = {'pdf'}

# Base de datos simulada (en producción, esto vendría de una base de datos real)
PREGUNTAS = {
    'cultura': [
        {
            'id': 1,
            'pregunta': "¿Cómo interpretan los Arhuacos el concepto de 'Ley de Origen' y cómo rige su vida cotidiana?",
            'opciones': [
                {'texto': "Es un conjunto de reglas escritas que deben seguirse al pie de la letra", 'es_correcta': False},
                {'texto': "Es un sistema de conocimiento ancestral que guía su relación con la naturaleza y la comunidad", 'es_correcta': True},
                {'texto': "Son tradiciones antiguas que ya no tienen relevancia en la actualidad", 'es_correcta': False}
            ],
            'explicacion': "La Ley de Origen es el fundamento de la cultura Arhuaca, un sistema de conocimiento que rige su relación con la naturaleza, la comunidad y el universo, transmitido por los Mamos."
        },
        {
            'id': 2,
            'pregunta': "¿Qué papel juegan los Mamos en la transmisión del conocimiento espiritual y la toma de decisiones comunitarias?",
            'opciones': [
                {'texto': "Son líderes políticos que toman decisiones unilaterales", 'es_correcta': False},
                {'texto': "Son guías espirituales que interpretan la Ley de Origen y orientan a la comunidad", 'es_correcta': True},
                {'texto': "Son ancianos sin un rol activo en la comunidad actual", 'es_correcta': False}
            ],
            'explicacion': "Los Mamos son autoridades espirituales que interpretan la Ley de Origen, guían a la comunidad y toman decisiones basadas en su sabiduría ancestral."
        },
        {
            'id': 3,
            'pregunta': "¿Por qué el algodón es considerado un elemento sagrado en su artesanía y vestimenta?",
            'opciones': [
                {'texto': "Porque es fácil de conseguir y trabajar", 'es_correcta': False},
                {'texto': "Porque representa la conexión entre la Madre Tierra y el pensamiento puro", 'es_correcta': True},
                {'texto': "Porque es resistente al clima de la Sierra Nevada", 'es_correcta': False}
            ],
            'explicacion': "El algodón es símbolo de pureza y pensamiento, usado en rituales y tejidos sagrados por los Arhuacos, representando la conexión con la Madre Tierra."
        },
        {
            'id': 4,
            'pregunta': "¿Cómo interpretan los Arhuacos los sueños como herramienta de guía espiritual y toma de decisiones?",
            'opciones': [
                {'texto': "Los consideran mensajes espirituales importantes que guían sus decisiones", 'es_correcta': True},
                {'texto': "Son solo experiencias aleatorias sin significado especial", 'es_correcta': False},
                {'texto': "Son vistos como supersticiones sin relevancia en la vida diaria", 'es_correcta': False}
            ],
            'explicacion': "Los sueños son considerados mensajes de los espíritus y ancestros, que los Mamos interpretan para guiar a la comunidad en la toma de decisiones importantes."
        }
    ],
    'practicas': [
        {
            'id': 5,
            'pregunta': "¿Por qué el poporo es un objeto sagrado para los Arhuacos y qué simboliza su uso en rituales?",
            'opciones': [
                {'texto': "Es un simple recipiente para guardar hojas de coca", 'es_correcta': False},
                {'texto': "Simboliza el útero femenino y la continuidad de la vida", 'es_correcta': True},
                {'texto': "Es un objeto decorativo sin mayor significado", 'es_correcta': False}
            ],
            'explicacion': "El poporo es un objeto ritual que representa el útero femenino y la continuidad de la vida. Su uso en rituales con hojas de coca y conchas molidas simboliza la armonía y el equilibrio cósmico."
        },
        {
            'id': 6,
            'pregunta': "¿Cómo se elaboran las mochilas Arhuacas y qué significan sus diseños y colores?",
            'opciones': [
                {'texto': "Son tejidas a mano con diseños que representan elementos de la naturaleza y la cosmovisión Arhuaca", 'es_correcta': True},
                {'texto': "Son compradas en el mercado con diseños modernos", 'es_correcta': False},
                {'texto': "Son hechas con máquinas de tejer industriales", 'es_correcta': False}
            ],
            'explicacion': "Las mochilas Arhuacas son tejidas a mano por las mujeres, con diseños que representan elementos de la naturaleza y la cosmovisión de su pueblo. Cada color y patrón tiene un significado espiritual y cultural profundo."
        },
        {
            'id': 7,
            'pregunta': "¿Cómo se prepara física y espiritualmente un joven Arhuaco para convertirse en Mamo?",
            'opciones': [
                {'texto': "Asistiendo a una universidad occidental", 'es_correcta': False},
                {'texto': "A través de un riguroso entrenamiento espiritual en las montañas sagradas", 'es_correcta': True},
                {'texto': "Participando en concursos de conocimiento", 'es_correcta': False}
            ],
            'explicacion': "Los futuros Mamos son seleccionados desde niños y pasan por un largo período de aislamiento en las montañas sagradas, donde aprenden los secretos de la naturaleza, la medicina tradicional y la sabiduría ancestral."
        },
        {
            'id': 8,
            'pregunta': "¿Qué papel juegan los cantos tradicionales (Iku) en los rituales de sanación?",
            'opciones': [
                {'texto': "Son solo entretenimiento durante las ceremonias", 'es_correcta': False},
                {'texto': "Son herramientas poderosas para la sanación física y espiritual", 'es_correcta': True},
                {'texto': "Son canciones populares sin propósito específico", 'es_correcta': False}
            ],
            'explicacion': "Los cantos tradicionales Iku son considerados herramientas poderosas de sanación que conectan al individuo con las fuerzas espirituales y ayudan a restaurar el equilibrio energético."
        }
    ],
    'sagrado': [
        {
            'id': 9,
            'pregunta': "¿Qué estrategias ha implementado el pueblo Arhuaco para defender su territorio ante proyectos extractivos?",
            'opciones': [
                {'texto': "Han abandonado sus territorios tradicionales", 'es_correcta': False},
                {'texto': "Han establecido sistemas de vigilancia comunitaria y acciones legales", 'es_correcta': True},
                {'texto': "Han permitido el ingreso de empresas mineras con ciertas condiciones", 'es_correcta': False}
            ],
            'explicacion': "Los Arhuacos han implementado diversas estrategias como la creación de guardias indígenas, acciones legales, y la difusión de su situación a nivel internacional para proteger sus territorios sagrados."
        },
        {
            'id': 10,
            'pregunta': "¿Cómo funciona su gobierno propio y qué rol juegan las guardias indígenas en la protección de la Sierra Nevada?",
            'opciones': [
                {'texto': "No tienen un sistema organizado de gobierno", 'es_correcta': False},
                {'texto': "Tienen una estructura de gobierno tradicional que incluye Mamos y autoridades comunitarias", 'es_correcta': True},
                {'texto': "Siguen las mismas leyes del gobierno colombiano sin adaptaciones", 'es_correcta': False}
            ],
            'explicacion': "Los Arhuacos tienen un sistema de gobierno propio basado en la Ley de Origen, donde los Mamos son las máximas autoridades espirituales y las decisiones se toman en asambleas comunitarias. Las guardias indígenas protegen el territorio de amenazas externas."
        },
        {
            'id': 11,
            'pregunta': "¿Cómo protegen los Arhuacos los lugares sagrados (como ríos y montañas) de amenazas externas (minería, turismo)?",
            'opciones': [
                {'texto': "Permiten el acceso controlado a turistas y empresas", 'es_correcta': False},
                {'texto': "Establecen cercas y restricciones de acceso basadas en su cosmovisión", 'es_correcta': True},
                {'texto': "No toman medidas especiales de protección", 'es_correcta': False}
            ],
            'explicacion': "Los Arhuacos protegen sus lugares sagrados a través de la educación comunitaria, la resistencia pacífica, y la aplicación de sus propias leyes ancestrales, limitando el acceso a estos espacios según su cosmovisión."
        },
        {
            'id': 12,
            'pregunta': "¿Cómo definen los Arhuacos los límites de la 'Línea Negra' y qué herramientas usan para protegerla?",
            'opciones': [
                {'texto': "Es un límite geopolítico establecido por el gobierno", 'es_correcta': False},
                {'texto': "Es un territorio sagrado que incluye sitios ceremoniales y ecosistemas vitales", 'es_correcta': True},
                {'texto': "Es una zona de explotación de recursos naturales", 'es_correcta': False}
            ],
            'explicacion': "La Línea Negra es un territorio sagrado que los Arhuacos definen como un espacio de equilibrio ecológico y espiritual, que incluye sitios ceremoniales, nacimientos de agua y ecosistemas vitales. La protegen mediante la vigilancia comunitaria y acciones legales."
        },
        {
            'id': 13,
            'pregunta': "¿Qué consecuencias espirituales creen que ocurrirían si un lugar sagrado como el río Guatapurí es contaminado?",
            'opciones': [
                {'texto': "No tiene consecuencias importantes", 'es_correcta': False},
                {'texto': "Puede romper el equilibrio espiritual y afectar la salud del pueblo", 'es_correcta': True},
                {'texto': "Solo afecta a los peces", 'es_correcta': False}
            ],
            'explicacion': "La contaminación de un río sagrado puede alterar el equilibrio del territorio y causar desarmonía espiritual según los Mamos, afectando tanto a la comunidad como al ecosistema en su conjunto."
        },
        {
            'id': 14,
            'pregunta': "¿Existen lugares sagrados compartidos con los pueblos Kogui, Wiwa o Kankuamo? ¿Cómo los gestionan?",
            'opciones': [
                {'texto': "No comparten lugares sagrados con otros pueblos", 'es_correcta': False},
                {'texto': "Sí, comparten sitios sagrados y los gestionan mediante acuerdos interétnicos", 'es_correcta': True},
                {'texto': "Cada pueblo tiene sus propios lugares sin coordinación entre ellos", 'es_correcta': False}
            ],
            'explicacion': "Los pueblos indígenas de la Sierra Nevada comparten algunos sitios sagrados y han establecido acuerdos interétnicos para su protección y gestión conjunta, respetando las tradiciones de cada pueblo."
        },
        {
            'id': 15,
            'pregunta': "¿Cómo se integra el conocimiento geográfico ancestral con los mapas digitales (SIG) en su lucha territorial?",
            'opciones': [
                {'texto': "Rechazan completamente la tecnología moderna", 'es_correcta': False},
                {'texto': "Combinan su conocimiento ancestral con tecnología SIG para documentar y proteger su territorio", 'es_correcta': True},
                {'texto': "Solo confían en la memoria oral sin registros físicos o digitales", 'es_correcta': False}
            ],
            'explicacion': "Los Arhuacos han aprendido a integrar los Sistemas de Información Geográfica (SIG) con su conocimiento ancestral para mapear y documentar su territorio, fortaleciendo así sus estrategias de defensa territorial y gestión ambiental."
        }
    ]
}

VIDEOS = [
    {
        'id': 1,
        'titulo': "La Ley de Origen - Sabiduría Arhuaca",
        'descripcion': "Documental sobre los principios fundamentales de la Ley de Origen en la cultura Arhuaca.",
        'url': "https://www.youtube.com/embed/L_yP7m_SaRc",
        'duracion': "15:30"
    },
    {
        'id': 2,
        'titulo': "Tejidos y Simbolismo",
        'descripcion': "El significado profundo de los tejidos tradicionales Arhuacos y su conexión con la naturaleza.",
        'url': "https://www.youtube.com/embed/Qu1FrjSGvX0",
        'duracion': "12:45"
    },
    {
        'id': 3,
        'titulo': "Rituales de la Sierra Nevada",
        'descripcion': "Una mirada respetuosa a los rituales sagrados de los pueblos de la Sierra Nevada.",
        'url': "https://www.youtube.com/embed/nv3_aPJ8GNk",
        'duracion': "18:20"
    }
]

# Simulación de base de datos de guías (en producción, esto estaría en una BD)
GUIAS = [
    {
        'id': 1,
        'titulo': "Guía de la Lengua Iku",
        'archivo': "guia_lengua_iku.pdf",
        'fecha': "2023-07-15",
        'tamano': 2.4,
        'categoria': 'lenguaje'
    },
    {
        'id': 2,
        'titulo': "Historia del Pueblo Arhuaco",
        'archivo': "historia_arhuacos.pdf",
        'fecha': "2023-06-01",
        'tamano': 3.1,
        'categoria': 'historia'
    }
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def formatear_tamano(bytes):
    """Convierte bytes a formato legible"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.1f} TB"

@modulo_bp.route('/modulo-educativo')
def modulo_educativo():
    """Página principal del módulo educativo"""
    # Calcular estadísticas
    total_preguntas = sum(len(preguntas) for preguntas in PREGUNTAS.values())
    total_guias = len(GUIAS)
    total_videos = len(VIDEOS)
    
    return render_template('institucional/modulo.html', 
                         total_preguntas=total_preguntas,
                         total_guias=total_guias,
                         total_videos=total_videos)

@modulo_bp.route('/api/preguntas/<categoria>')
def obtener_preguntas(categoria):
    """API para obtener preguntas por categoría"""
    try:
        preguntas = PREGUNTAS.get(categoria, [])
        return jsonify({
            'success': True,
            'preguntas': preguntas,
            'categoria': categoria,
            'total': len(preguntas)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error al obtener preguntas: {str(e)}'
        }), 500

@modulo_bp.route('/api/videos')
def obtener_videos():
    """API para obtener lista de videos"""
    try:
        return jsonify({
            'success': True,
            'videos': VIDEOS,
            'total': len(VIDEOS)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error al obtener videos: {str(e)}'
        }), 500

@modulo_bp.route('/api/guias')
def obtener_guias():
    """API para obtener lista de guías"""
    try:
        guias_con_formato = []
        for guia in GUIAS:
            guia_formateada = guia.copy()
            # Formatear fecha
            if isinstance(guia['fecha'], str):
                fecha_obj = datetime.strptime(guia['fecha'], '%Y-%m-%d')
                guia_formateada['fecha_formateada'] = fecha_obj.strftime('%d/%m/%Y')
            else:
                guia_formateada['fecha_formateada'] = guia['fecha']
            
            # Formatear tamaño
            if isinstance(guia['tamano'], (int, float)):
                guia_formateada['tamano_formateado'] = f"{guia['tamano']} MB"
            else:
                guia_formateada['tamano_formateado'] = str(guia['tamano'])
            
            guias_con_formato.append(guia_formateada)
        
        return jsonify({
            'success': True,
            'guias': guias_con_formato,
            'total': len(guias_con_formato)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error al obtener guías: {str(e)}'
        }), 500

# Ruta principal para subir guías (que usa el frontend)
@modulo_bp.route('/api/subir-guia', methods=['POST'])
def subir_guia():
    """API para subir una nueva guía"""
    if 'user_admin' not in session:
        return jsonify({'success': False, 'mensaje': 'No tienes permisos para subir guías'})
    
    try:
        # Validar que se enviaron los datos requeridos
        if 'titulo' not in request.form or 'categoria' not in request.form:
            return jsonify({'success': False, 'mensaje': 'Faltan campos requeridos'})
        
        if 'archivo' not in request.files:
            return jsonify({'success': False, 'mensaje': 'No se seleccionó ningún archivo'})
        
        archivo = request.files['archivo']
        titulo = request.form['titulo'].strip()
        categoria = request.form['categoria']
        
        # Validaciones
        if archivo.filename == '':
            return jsonify({'success': False, 'mensaje': 'No se seleccionó ningún archivo'})
        
        if not titulo:
            return jsonify({'success': False, 'mensaje': 'El título es requerido'})
        
        if not categoria:
            return jsonify({'success': False, 'mensaje': 'La categoría es requerida'})
        
        if not allowed_file(archivo.filename):
            return jsonify({'success': False, 'mensaje': 'Solo se permiten archivos PDF'})
        
        # Crear directorio si no existe
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Generar nombre único para el archivo
        filename = secure_filename(archivo.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = f"{timestamp}_{filename}"
        archivo_path = os.path.join(UPLOAD_FOLDER, nombre_archivo)
        
        # Guardar el archivo
        archivo.save(archivo_path)
        
        # Obtener el tamaño del archivo
        tamano_bytes = os.path.getsize(archivo_path)
        tamano_mb = round(tamano_bytes / (1024 * 1024), 1)
        
        # Crear nueva guía
        nueva_guia = {
            'id': max([g['id'] for g in GUIAS], default=0) + 1,
            'titulo': titulo,
            'categoria': categoria,
            'archivo': nombre_archivo,
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'tamano': tamano_mb
        }
        
        # Agregar a la lista (al principio para que aparezca primero)
        GUIAS.insert(0, nueva_guia)
        
        return jsonify({'success': True, 'mensaje': 'Guía subida correctamente'})
        
    except Exception as e:
        return jsonify({'success': False, 'mensaje': f'Error al subir la guía: {str(e)}'})

# Ruta alternativa (mantener compatibilidad)
@modulo_bp.route('/api/guias/subir', methods=['POST'])
def subir_guia_alt():
    """API alternativa para subir guías"""
    return subir_guia()

@modulo_bp.route('/api/responder-pregunta', methods=['POST'])
def responder_pregunta():
    """API para procesar respuesta a una pregunta"""
    try:
        data = request.get_json()
        pregunta_id = data.get('pregunta_id')
        opcion_seleccionada = data.get('opcion_seleccionada')
        categoria = data.get('categoria')
        
        # Buscar la pregunta
        preguntas_categoria = PREGUNTAS.get(categoria, [])
        pregunta = next((p for p in preguntas_categoria if p['id'] == pregunta_id), None)
        
        if not pregunta:
            return jsonify({
                'success': False,
                'mensaje': 'Pregunta no encontrada'
            }), 404
        
        # Verificar respuesta
        if opcion_seleccionada >= len(pregunta['opciones']):
            return jsonify({
                'success': False,
                'mensaje': 'Opción inválida'
            }), 400
        
        es_correcta = pregunta['opciones'][opcion_seleccionada]['es_correcta']
        respuesta_correcta_idx = next(i for i, op in enumerate(pregunta['opciones']) if op['es_correcta'])
        
        return jsonify({
            'success': True,
            'es_correcta': es_correcta,
            'respuesta_correcta': respuesta_correcta_idx,
            'explicacion': pregunta['explicacion'],
            'opcion_seleccionada': opcion_seleccionada
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error al procesar respuesta: {str(e)}'
        }), 500

@modulo_bp.route('/api/descargar-guia/<int:guia_id>')
def descargar_guia(guia_id):
    """API para descargar una guía específica"""
    try:
        guia = next((g for g in GUIAS if g['id'] == guia_id), None)
        
        if not guia:
            return jsonify({
                'success': False,
                'mensaje': 'Guía no encontrada'
            }), 404
        
        archivo_path = os.path.join(UPLOAD_FOLDER, guia['archivo'])
        
        if not os.path.exists(archivo_path):
            return jsonify({
                'success': False,
                'mensaje': 'Archivo no encontrado en el servidor'
            }), 404
        
        return send_file(archivo_path, as_attachment=True, download_name=guia['archivo'])
        
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error al descargar guía: {str(e)}'
        }), 500

@modulo_bp.route('/api/editar-guia/<int:guia_id>', methods=['PUT'])
def editar_guia(guia_id):
    """API para editar una guía existente"""
    if 'user_admin' not in session:
        return jsonify({'success': False, 'mensaje': 'No tienes permisos para editar guías'})
    
    try:
        data = request.get_json()
        nuevo_titulo = data.get('titulo', '').strip()
        nueva_categoria = data.get('categoria', 'general')
        
        if not nuevo_titulo:
            return jsonify({
                'success': False,
                'mensaje': 'El título es requerido'
            }), 400
        
        # Buscar la guía
        guia = next((g for g in GUIAS if g['id'] == guia_id), None)
        
        if not guia:
            return jsonify({
                'success': False,
                'mensaje': 'Guía no encontrada'
            }), 404
        
        # Actualizar los datos
        guia['titulo'] = nuevo_titulo
        guia['categoria'] = nueva_categoria
        
        return jsonify({
            'success': True,
            'mensaje': 'Guía actualizada correctamente'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error al editar guía: {str(e)}'
        }), 500

@modulo_bp.route('/api/eliminar-guia/<int:guia_id>', methods=['DELETE'])
def eliminar_guia(guia_id):
    """API para eliminar una guía específica"""
    if 'user_admin' not in session:
        return jsonify({'success': False, 'mensaje': 'No tienes permisos para eliminar guías'})
    
    try:
        # Buscar la guía
        guia = next((g for g in GUIAS if g['id'] == guia_id), None)
        
        if not guia:
            return jsonify({
                'success': False,
                'mensaje': 'Guía no encontrada'
            }), 404
        
        # Eliminar archivo físico del servidor si existe
        archivo_path = os.path.join(UPLOAD_FOLDER, guia['archivo'])
        if os.path.exists(archivo_path):
            try:
                os.remove(archivo_path)
            except OSError as e:
                print(f"Error al eliminar archivo: {e}")
        
        # Eliminar de la lista
        GUIAS.remove(guia)
        
        return jsonify({
            'success': True,
            'mensaje': 'Guía eliminada correctamente'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error al eliminar guía: {str(e)}'
        }), 500

@modulo_bp.route('/api/estadisticas')
def obtener_estadisticas():
    """API para obtener estadísticas del módulo educativo"""
    try:
        total_preguntas = sum(len(preguntas) for preguntas in PREGUNTAS.values())
        estadisticas_por_categoria = {
            categoria: len(preguntas) 
            for categoria, preguntas in PREGUNTAS.items()
        }
        
        return jsonify({
            'success': True,
            'estadisticas': {
                'total_preguntas': total_preguntas,
                'total_guias': len(GUIAS),
                'total_videos': len(VIDEOS),
                'preguntas_por_categoria': estadisticas_por_categoria
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'mensaje': f'Error al obtener estadísticas: {str(e)}'
        }), 500
