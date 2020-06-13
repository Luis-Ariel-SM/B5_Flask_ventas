from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError



class ProductForm(FlaskForm):
    id = HiddenField('id') # Campo oculto, no aparecera visualmente pero si viajara el dato con las peticiones del navegador
    tipo_producto = StringField('Tipo de producto', validators=[DataRequired(), Length(min=3, message='Debe tener al menos tres caracteres')])
    precio_unitario = FloatField ('Precio unitario', validators=[DataRequired(message='Debe tener un precio y solo en valores numericos')])
    coste_unitario = FloatField ('Coste unitario', validators=[DataRequired(message='Debe tener un coste y solo en valores numericos')])

    submit = SubmitField('Aceptar')


    # Validador especifico hecho a medida segun sintaxis de los formularios de flask
    def validate_coste_unitario(self, field): # Primer parametro es el formulario (funciona como el self de los objetos) y el segundo es el propio campo, que en coste_unitario es un "FloadField"
        if field.data > self.precio_unitario.data:
            raise ValidationError ('El coste unitario ha de ser menor o igual que el precio unitario')

class ModProductForm(FlaskForm):
    id = HiddenField('id')
    tipo_producto = StringField('Tipo de producto', validators=[DataRequired(), Length(min=3, message='Debe tener al menos tres caracteres')])
    precio_unitario = FloatField ('Precio unitario', validators=[DataRequired(message='Debe tener un precio y solo en valores numericos')])
    coste_unitario = FloatField ('Coste unitario', validators=[DataRequired(message='Debe tener un coste y solo en valores numericos')])

    modificar = SubmitField('Modificar')
    borrar = SubmitField('Borrar')

    def validate_coste_unitario(self, field): 
        if field.data > self.precio_unitario.data:
            raise ValidationError ('El coste unitario ha de ser menor o igual que el precio unitario')


