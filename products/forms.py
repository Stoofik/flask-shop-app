from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import IntegerField, StringField, BooleanField, TextAreaField, SubmitField, DecimalField, validators
from wtforms.validators import DataRequired, Email, Length, EqualTo

class Addproducts(FlaskForm):
    name = StringField("Název", validators=[DataRequired()])
    price = DecimalField("Cena", validators=[DataRequired()])
    discount = IntegerField("Sleva", default=0)
    stock = IntegerField("Množství na skladě", validators=[DataRequired()])
    description = TextAreaField("Popis", validators=[DataRequired()])
    colors = TextAreaField("Barva", validators=[DataRequired()])
    submit = SubmitField("Přidat produkt")

    image_1 = FileField("Obrázek  1", validators=[FileAllowed(["jpg", "png", "gif", "jpeg", "svg"])])
    image_2 = FileField("Obrázek 2", validators=[FileAllowed(["jpg", "png", "gif", "jpeg", "svg"])])
    image_3 = FileField("Obrázek 3", validators=[FileAllowed(["jpg", "png", "gif", "jpeg", "svg"])])



