from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField("Uživatelské jméno", validators=[DataRequired(message="Zadejte uživatelské jméno"), Length(min=2,max=20, message="Uživatelské jméno musí být mezi 2 a 20 znaky")])
    email = StringField("Email", validators=[DataRequired(), Email(message="Zadejte platný email")])
    password = PasswordField("Heslo", validators=[DataRequired(), Length(min=8, max=25, message="Heslo musí být v rozmezí 8 až 25 znaků")])
    confirm_password = PasswordField("Potvrdit heslo", validators=[DataRequired(), EqualTo("password", message="Hesla se musí shodovat")])

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(message="Zadejte platný email")])
    password = PasswordField("Heslo", validators=[DataRequired()])