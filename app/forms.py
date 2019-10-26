from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Felhasználónév', validators=[DataRequired()])
    password = PasswordField('Jelszó', validators=[DataRequired()])
    remember_me = BooleanField('Emlékezz rám')
    submit = SubmitField('Bejelentkezés')
#todo: to english

class RegistrationForm(FlaskForm):
    username = StringField('Felhasználónév', validators=[DataRequired()])
    email = StringField('Email cím', validators=[DataRequired(), Email()])
    password = PasswordField('Jelszó', validators=[DataRequired()])
    password2 = PasswordField('Jelszó mégegyszer', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Regisztrálok')
    # todo to english, expand with stuff

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Kérlek válassz másik felhasználónevet!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Kérlek válassz másik email-címet!')

