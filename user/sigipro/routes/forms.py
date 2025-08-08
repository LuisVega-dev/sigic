from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistroForm(FlaskForm):
    """Formulario para registro de nuevos usuarios con validación y protección CSRF."""
    nombre = StringField('Nombre completo', validators=[DataRequired(message='El nombre es obligatorio')])
    correo = EmailField('Correo electrónico', validators=[
        DataRequired(message='El correo es obligatorio'),
        Email(message='Ingresa un correo válido')
    ])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(message='La contraseña es obligatoria')])
    confirmar_contraseña = PasswordField('Confirmar contraseña', validators=[
        DataRequired(message='Confirma tu contraseña'),
        EqualTo('contraseña', message='Las contraseñas deben coincidir')
    ])
    imagen = FileField('Imagen de perfil (opcional)')
    submit = SubmitField('Registrarse')

class PerfilForm(FlaskForm):
    """Formulario para editar perfil de usuario"""
    nombre_completo = StringField('Nombre Completo', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefono = StringField('Teléfono')
    direccion = StringField('Dirección')
    biografia = TextAreaField('Biografía')
    foto_perfil = FileField('Foto de Perfil')
    submit = SubmitField('Guardar Cambios')