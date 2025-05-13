from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FileField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from .models.users import Users

class RegistrationForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=2, max=20)])
    sec_name = StringField('Фамилия', validators=[DataRequired(), Length(min=2, max=50)])
    name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=50)])
    otch = StringField('Отчество', validators=[Length(min=2, max=50)])
    passw = PasswordField('Пароль', validators=[DataRequired()])
    passw_conf = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('passw')])
    scans = FileField('Загрузить скан документа', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Зарегистрировться')

    def validate_login(self, login):
        user = Users.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError('Данное имя пользователя уже используется. Поджалуйста, выберите другое')

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=2, max=20)])
    passw = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class StuffForm(FlaskForm):
    stuff = SelectField('stuff', choices=[], render_kw={'class':'form-control'})

