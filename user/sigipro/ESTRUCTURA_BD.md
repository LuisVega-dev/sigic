# Estructura de la Base de Datos - SIGIPRO

## Tabla: usuario

### Columnas existentes:

- `id` (INT, PRIMARY KEY, AUTO_INCREMENT) - ID único del usuario
- `nombre` (VARCHAR) - Nombre completo del usuario
- `correo` (VARCHAR, UNIQUE) - Correo electrónico del usuario
- `contraseña` (VARCHAR) - Contraseña encriptada con hash
- `imagen` (VARCHAR, NULLABLE) - Nombre del archivo de imagen de perfil

### Columnas adicionales requeridas:

Para que el sistema funcione completamente, ejecutar el siguiente SQL:

```sql
USE sigic;

-- Agregar columnas adicionales si no existen
ALTER TABLE usuario ADD COLUMN telefono VARCHAR(20) NULL;
ALTER TABLE usuario ADD COLUMN direccion TEXT NULL;
ALTER TABLE usuario ADD COLUMN biografia TEXT NULL;
```

### Variables de sesión utilizadas:

- `session['user_id']` - ID del usuario autenticado
- `session['user_name']` - Nombre del usuario
- `session['usuario']` - Alias para compatibilidad con plantillas
- `session['user_image']` - Ruta de la imagen de perfil

### Templates actualizados:

- `perfil.html` - Muestra solo campos existentes en la BD
- `editar_perfil.html` - Usa el campo correcto `imagen` en lugar de `foto_perfil`
- `navbar.html` - Corregida referencia a `url_for('perfil')`

### Formularios implementados:

- `RegistroForm` - Con protección CSRF y validación
- `PerfilForm` - Para editar datos del usuario

### Rutas corregidas:

- `/perfil` - Ver perfil del usuario
- `/perfil/editar` - Editar perfil del usuario
