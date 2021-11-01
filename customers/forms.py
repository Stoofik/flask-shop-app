from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf.file import FileRequired, FileAllowed, FileField
from .models import Register


class CustomerRegisterForm(FlaskForm):
    username =  StringField("Uživatelské jméno*", validators=[DataRequired(message="Zadejte Vaše uživatelské jméno"), Length(min=2, max=25, message="Uživatelské jméno musí být mezi 2 a 20 znaky")])
    email = StringField("Email*", validators=[DataRequired(), Email(message="Zadejte platný email")])
    password = PasswordField("Heslo*",  validators=[DataRequired(message="Zadejte heslo"), Length(min=8, max=25, message="Heslo musí mít alespoň 8 znaků")])
    confirm_password = PasswordField("Potvrdit heslo*", validators=[DataRequired(), EqualTo("password", message="Hesla se musí shodovat")])
    
    surname = StringField("Křestní jméno*", validators=[DataRequired(message="Zadejte Vaše křestní jméno"), Length(min=2, max=25, message="Křestní jméno musí být mezi 2 a 20 znaky")])
    last_name = StringField("Příjmení*", validators=[DataRequired(message="Zadejte Vaše příjmení"), Length(min=2, max=25, message="Příjmení musí být mezi 2 a 20 znaky")])
    contact = StringField("Telefon*", validators=[DataRequired(message="Telefon potřebujeme pro rychlou komunikaci v případě potíží")])
    country = StringField("Země*", validators=[DataRequired(message="Zemi potřebujeme, protože posíláme i na Slovensko!")])
    city = StringField("Město*", validators=[DataRequired(message="Zadejte Vaše město")])
    adress = StringField ("Ulice a číslo popisné*", validators=[DataRequired(message="Zadejte adresu a číslo popisné")])
    zipcode = StringField("PSČ*", validators=[DataRequired(message="Zadejte poštovní směrovací číslo")])
    
    submit = SubmitField("Zaregistrovat")

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("Toto uživatelské jméno již někdo používá")


    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("Tento email již je zaregistrovaný")


class CustomerLoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(message="Zadejte platný email")])
    password = PasswordField("Heslo",  validators=[DataRequired(message="Zadejte heslo")])
    submit = SubmitField("Přihlásit se")


class UpdateAccountForm(FlaskForm):
    username =  StringField("Uživatelské jméno*", validators=[DataRequired(message="Zadejte Vaše uživatelské jméno"), Length(min=2, max=25, message="Uživatelské jméno musí být mezi 2 a 20 znaky")])
    email = StringField("Email*", validators=[DataRequired(), Email(message="Zadejte platný email")])
    surname = StringField("Křestní jméno*", validators=[DataRequired(message="Zadejte Vaše křestní jméno"), Length(min=2, max=25, message="Křestní jméno musí být mezi 2 a 20 znaky")])
    last_name = StringField("Příjmení*", validators=[DataRequired(message="Zadejte Vaše příjmení"), Length(min=2, max=25, message="Příjmení musí být mezi 2 a 20 znaky")])
    contact = StringField("Telefon*", validators=[DataRequired(message="Telefon potřebujeme pro rychlou komunikaci v případě potíží")])
    country = StringField("Země*", validators=[DataRequired(message="Zemi potřebujeme, protože posíláme i na Slovensko!")])
    city = StringField("Město*", validators=[DataRequired(message="Zadejte Vaše město")])
    adress = StringField ("Ulice a číslo popisné*", validators=[DataRequired(message="Zadejte adresu a číslo popisné")])
    zipcode = StringField("PSČ*", validators=[DataRequired(message="Zadejte poštovní směrovací číslo")])

    def validate_username(self, username):
        if username.data != current_user.username:
            if Register.query.filter_by(username=username.data).first():
                raise ValidationError("Toto uživatelské jméno již někdo používá")


    def validate_email(self, email):
        if email.data != current_user.email:
            if Register.query.filter_by(email=email.data).first():
                raise ValidationError("Tento email již je zaregistrovaný")


