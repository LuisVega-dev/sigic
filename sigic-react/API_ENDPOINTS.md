# Configuración de Endpoints para el Sistema SIGIC

Este documento describe los endpoints necesarios para que el frontend funcione correctamente con el menú de navegación.

## Endpoints Requeridos

### 1. Usuarios

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

### 2. Productos

- **URL**: `http://127.0.0.1:5000/api/productos`
- **Método**: GET
- **Respuesta esperada**:

```json
[
  {
    "id": 1,
    "nombre": "Laptop Dell",
    "precio": 1200.0,
    "categoria": "Electrónicos"
  },
  {
    "id": 2,
    "nombre": "Mouse Logitech",
    "precio": 25.99,
    "categoria": "Accesorios"
  }
]
```

### 3. Clientes

- **URL**: `http://127.0.0.1:5000/api/clientes`
- **Método**: GET
- **Respuesta esperada**:

```json
[
  {
    "id": 1,
    "nombre": "Empresa ABC S.A.",
    "telefono": "+1234567890",
    "direccion": "Calle Principal 123"
  },
  {
    "id": 2,
    "nombre": "Comercial XYZ Ltda.",
    "telefono": "+0987654321",
    "direccion": "Avenida Central 456"
  }
]
```

### 4. Ventas

- **URL**: `http://127.0.0.1:5000/api/ventas`
- **Método**: GET
- **Respuesta esperada**:

```json
[
  {
    "id": 1,
    "fecha": "2025-07-04T10:30:00Z",
    "cliente": "Empresa ABC S.A.",
    "total": 1500.0
  },
  {
    "id": 2,
    "fecha": "2025-07-03T14:15:00Z",
    "cliente": "Comercial XYZ Ltda.",
    "total": 850.5
  }
]
```

## Ejemplo de Implementación en Flask

```python
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/usuarios')
def get_usuarios():
    usuarios = [
        {"id": 1, "nombre": "Juan Pérez", "correo": "juan@example.com"},
        {"id": 2, "nombre": "María García", "correo": "maria@example.com"},
        {"id": 3, "nombre": "Carlos López", "correo": "carlos@example.com"}
    ]
    return jsonify(usuarios)

@app.route('/api/productos')
def get_productos():
    productos = [
        {"id": 1, "nombre": "Laptop Dell", "precio": 1200.00, "categoria": "Electrónicos"},
        {"id": 2, "nombre": "Mouse Logitech", "precio": 25.99, "categoria": "Accesorios"},
        {"id": 3, "nombre": "Teclado Mecánico", "precio": 85.50, "categoria": "Accesorios"}
    ]
    return jsonify(productos)

@app.route('/api/clientes')
def get_clientes():
    clientes = [
        {"id": 1, "nombre": "Empresa ABC S.A.", "telefono": "+1234567890", "direccion": "Calle Principal 123"},
        {"id": 2, "nombre": "Comercial XYZ Ltda.", "telefono": "+0987654321", "direccion": "Avenida Central 456"},
        {"id": 3, "nombre": "Distribuidora 123", "telefono": "+1122334455", "direccion": "Boulevard Norte 789"}
    ]
    return jsonify(clientes)

@app.route('/api/ventas')
def get_ventas():
    ventas = [
        {"id": 1, "fecha": "2025-07-04T10:30:00Z", "cliente": "Empresa ABC S.A.", "total": 1500.00},
        {"id": 2, "fecha": "2025-07-03T14:15:00Z", "cliente": "Comercial XYZ Ltda.", "total": 850.50},
        {"id": 3, "fecha": "2025-07-02T09:45:00Z", "cliente": "Distribuidora 123", "total": 2300.75}
    ]
    return jsonify(ventas)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
```

## Características del Frontend

### Funcionalidades Implementadas:

- ✅ Menú de navegación por pestañas
- ✅ Carga dinámica de datos desde diferentes APIs
- ✅ Tabla responsive que se adapta al tipo de datos
- ✅ Estados de carga, error y datos vacíos
- ✅ Formateo personalizado de datos (IDs, precios, fechas)
- ✅ Contadores dinámicos por tipo de datos
- ✅ Diseño futurista y moderno

### Pestañas Disponibles:

1. **Usuarios**: Muestra ID, Nombre y Correo Electrónico
2. **Productos**: Muestra ID, Producto, Precio y Categoría
3. **Clientes**: Muestra ID, Cliente, Teléfono y Dirección
4. **Ventas**: Muestra ID, Fecha, Cliente y Total

### Personalización:

Para agregar nuevas pestañas, simplemente modifica el objeto `tabs` en `App.jsx`:

```javascript
nuevaTab: {
  label: 'Nueva Tab',
  endpoint: 'http://127.0.0.1:5000/api/nueva-tab',
  columns: [
    { key: 'id', label: 'ID', render: (value) => `#${value.toString().padStart(3, '0')}` },
    { key: 'campo1', label: 'Campo 1' },
    { key: 'campo2', label: 'Campo 2', render: (value) => `Formato: ${value}` }
  ]
}
```
