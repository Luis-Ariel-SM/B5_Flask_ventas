from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError



class ProductForm(FlaskForm):
    tipo_producto = StringField('Tipo de producto', validators=[DataRequired(), Length(min=3, message='Debe tener al menos tres caracteres')])
    precio_unitario = FloatField ('Precio unitario', validators=[DataRequired(message='Bajanda')])
    coste_unitario = FloatField ('Coste unitario', validators=[DataRequired()])

    submit = SubmitField('Aceptar')


    # Validador especifico hecho a medida segun sintaxis de los formularios de flask
    def validate_coste_unitario(self, field): # Primer parametro es el formulario (funciona como el self de los objetos) y el segundo es el propio campo, que en coste_unitario es un "FloadField"
        if field.data > self.precio_unitario.data:
            raise ValidationError ('El coste unitario ha de ser menor o igual que el precio unitario')

