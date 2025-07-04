# Configuración de Endpoints para el Sistema SIGIC - CRUD Completo

Este documento describe todos los endpoints necesarios para que el frontend funcione correctamente con las operaciones CRUD (Crear, Leer, Actualizar, Eliminar).

## Endpoints Implementados

### 1. Usuarios

#### Obtener todos los usuarios

- **URL**: `http://127.0.0.1:5000/api/usuarios`
- **Método**: GET
- **Respuesta esperada**:

```json
[
  {
    "id": 1,
    "nombre": "Juan Pérez",
    "correo": "juan@example.com"
  },
  {
    "id": 2,
    "nombre": "María García",
    "correo": "maria@example.com"
  }
]
```

#### Actualizar un usuario

- **URL**: `http://127.0.0.1:5000/api/usuarios/{id}`
- **Método**: PUT
- **Headers**: `Content-Type: application/json`
- **Body**:

```json
{
  "nombre": "Juan Pérez Actualizado",
  "correo": "juan.nuevo@example.com"
}
```

- **Respuesta esperada**:

```json
{
  "id": 1,
  "nombre": "Juan Pérez Actualizado",
  "correo": "juan.nuevo@example.com"
}
```

#### Eliminar un usuario

- **URL**: `http://127.0.0.1:5000/api/usuarios/{id}`
- **Método**: DELETE
- **Respuesta esperada**: Status 200 o 204

### 2. Editores

#### Obtener todos los editores

- **URL**: `http://127.0.0.1:5000/api/editors`
- **Método**: GET
- **Respuesta esperada**:

```json
[
  {
    "id": 1,
    "nombre": "Admin Principal",
    "correo": "admin@example.com"
  },
  {
    "id": 2,
    "nombre": "Editor Secundario",
    "correo": "editor@example.com"
  }
]
```

#### Actualizar un editor

- **URL**: `http://127.0.0.1:5000/api/editors/{id}`
- **Método**: PUT
- **Headers**: `Content-Type: application/json`
- **Body**:

```json
{
  "nombre": "Admin Principal Actualizado",
  "correo": "admin.nuevo@example.com"
}
```

#### Eliminar un editor

- **URL**: `http://127.0.0.1:5000/api/editors/{id}`
- **Método**: DELETE
- **Respuesta esperada**: Status 200 o 204

## Ejemplo de Implementación en Flask

```python
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Datos de ejemplo (en producción usarías una base de datos)
usuarios = [
    {"id": 1, "nombre": "Juan Pérez", "correo": "juan@example.com"},
    {"id": 2, "nombre": "María García", "correo": "maria@example.com"},
    {"id": 3, "nombre": "Carlos López", "correo": "carlos@example.com"}
]

editores = [
    {"id": 1, "nombre": "Admin Principal", "correo": "admin@example.com"},
    {"id": 2, "nombre": "Editor Secundario", "correo": "editor@example.com"}
]

# ===== ENDPOINTS PARA USUARIOS =====

@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    return jsonify(usuarios)

@app.route('/api/usuarios/<int:user_id>', methods=['PUT'])
def update_usuario(user_id):
    data = request.get_json()

    # Buscar el usuario
    for i, usuario in enumerate(usuarios):
        if usuario['id'] == user_id:
            # Actualizar campos
            if 'nombre' in data:
                usuarios[i]['nombre'] = data['nombre']
            if 'correo' in data:
                usuarios[i]['correo'] = data['correo']

            return jsonify(usuarios[i])

    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/api/usuarios/<int:user_id>', methods=['DELETE'])
def delete_usuario(user_id):
    global usuarios
    usuarios = [u for u in usuarios if u['id'] != user_id]
    return '', 204

# ===== ENDPOINTS PARA EDITORES =====

@app.route('/api/editors', methods=['GET'])
def get_editores():
    return jsonify(editores)

@app.route('/api/editors/<int:editor_id>', methods=['PUT'])
def update_editor(editor_id):
    data = request.get_json()

    # Buscar el editor
    for i, editor in enumerate(editores):
        if editor['id'] == editor_id:
            # Actualizar campos
            if 'nombre' in data:
                editores[i]['nombre'] = data['nombre']
            if 'correo' in data:
                editores[i]['correo'] = data['correo']

            return jsonify(editores[i])

    return jsonify({"error": "Editor no encontrado"}), 404

@app.route('/api/editors/<int:editor_id>', methods=['DELETE'])
def delete_editor(editor_id):
    global editores
    editores = [e for e in editores if e['id'] != editor_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
```

## Características del Frontend

### Funcionalidades CRUD Implementadas:

- ✅ **Leer (Read)**: Visualización de datos en tabla responsive
- ✅ **Actualizar (Update)**: Modal de edición con formulario
- ✅ **Eliminar (Delete)**: Confirmación y eliminación con API
- ✅ Navegación por pestañas entre diferentes tipos de datos
- ✅ Estados de carga durante operaciones
- ✅ Manejo de errores con mensajes informativos
- ✅ Confirmación antes de eliminar
- ✅ Validación de formularios
- ✅ Interfaz moderna y responsive

### Componentes UI:

1. **Botones de Acción**: Editar (✏️) y Eliminar (🗑️) por cada fila
2. **Modal de Edición**: Formulario popup para modificar datos
3. **Confirmaciones**: Alertas antes de eliminar elementos
4. **Estados de Carga**: Indicadores durante operaciones CRUD

### Personalización:

Para agregar nuevas entidades, modifica el objeto `tabs` en `App.jsx`:

```javascript
nuevaEntidad: {
  label: 'Nueva Entidad',
  endpoint: 'http://127.0.0.1:5000/api/nueva-entidad',
  columns: [
    { key: 'id', label: 'ID', render: (value) => `#${value.toString().padStart(3, '0')}`, editable: false },
    { key: 'campo1', label: 'Campo 1', editable: true, type: 'text' },
    { key: 'campo2', label: 'Campo 2', editable: true, type: 'email' }
  ]
}
```

### Tipos de Input Soportados:

- `text`: Campo de texto normal
- `email`: Campo de email con validación
- `number`: Campo numérico
- `date`: Campo de fecha
- `tel`: Campo de teléfono

¡El sistema está listo para operaciones CRUD completas! 🚀
