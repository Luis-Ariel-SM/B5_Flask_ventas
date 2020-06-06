from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length


class ProductForm(FlaskForm):
    tipo_producto = StringField('Tipo de producto', validators=[DataRequired(), Length(min=3, message='Debe tener al menos tres caracteres')])
    precio_unitario = FloatField ('Precio unitario', validators=[DataRequired()])
    coste_unitario = FloatField ('Coste unitario', validators=[DataRequired()])

    submit = SubmitField('Aceptar')
