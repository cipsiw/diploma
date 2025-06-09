from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, FileField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from .models.users import Users

class RegistrationForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=2, max=20)])
    sec_name = StringField('Фамилия', validators=[DataRequired(), Length(min=2, max=50)])
    name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=50)])
    otch = StringField('Отчество', validators=[Length(min=2, max=50)])
    passw = PasswordField('Пароль', validators=[DataRequired()])
    passw_conf = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('passw')])
    scans = StringField()
    submit = SubmitField('Зарегистрироваться')

    def validate_login(self, login):
        user = Users.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError('Данное имя пользователя уже используется. Поджалуйста, выберите другое')
    def validate_inn(self, login):
        useri = Users.query.filter_by(login=login.data).first()
        if useri:
            raise ValidationError('Данный ИНН уже зарегистрирован')


class UserEdit(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=2, max=20)])
    sec_name = StringField('Фамилия', validators=[DataRequired(), Length(min=2, max=50)])
    name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=50)])
    otch = StringField('Отчество', validators=[Length(min=2, max=50)])
    passw = PasswordField('Пароль (оставьте пустым, чтобы не изменять)')
    passw_conf = PasswordField('Подтверждение пароля', validators=[EqualTo('passw', message='Пароли должны совпадать')])
    scans = StringField()
    role = SelectField('Роль', choices=[('admin', 'Администратор'),
                                        ('stuff', 'Сотрудник'),
                                        ('client', 'Клиент')],
                         render_kw={'class': 'form-control'})
    submit = SubmitField('Сохранить изменения')

    def validate_login(self, login):
        user = Users.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError('Данное имя пользователя уже используется. Поджалуйста, выберите другое')

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=2, max=20)])
    passw = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class ListForm(FlaskForm):
    stuff = SelectField('Сотрудник', choices=[('', 'Выберите сотрудника')], render_kw={'class':'form-control'}, validators=[DataRequired()])
    service = SelectField('Услуга', choices=[('', 'Выберите услугу')], render_kw={'class':'form-control'}, validators=[DataRequired()])
    client = SelectField('Клиент', choices=[('', 'Выберите клиента')], render_kw={'class': 'form-control'}, validators=[DataRequired()])

class RequestForm(FlaskForm):
    document = FileField('Прикрепить документ', validators=[FileAllowed(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'], message='Разрешены: PDF, Word, JPG, PNG')])

class RequestEditForm(FlaskForm):
    client = SelectField('Клиент', choices=[], render_kw={'class': 'form-control'})
    service = SelectField('Услуга', choices=[], render_kw={'class': 'form-control'})
    stuff = SelectField('Сотрудник', choices=[], render_kw={'class': 'form-control'})
    status = SelectField('Состояние', choices=[('Запланирована', 'Запланирована'),
                                               ('В работе', 'В работе'),
                                               ('Выполнена', 'Выполнена'),
                                               ('Отменена', 'Отменена')],
                         render_kw={'class': 'form-control'})
    document = FileField('Заменить документ', validators=[FileAllowed(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])])
    delete_document = BooleanField('Удалить текущий документ')
    submit = SubmitField('Сохранить изменения')

class CategAdd(FlaskForm):
    name = StringField('Наименование категории', validators=[DataRequired(), Length(min=2, max=150)])
    reqs = StringField('Требования', validators=[DataRequired(), Length(min=2, max=250)])
    submit = SubmitField('Добавить')

class CategEdit(FlaskForm):
    name = StringField('Наименование категории', validators=[DataRequired(), Length(min=2, max=150)])
    reqs = StringField('Требования', validators=[DataRequired(), Length(min=2, max=250)])
    submit = SubmitField('Сохранить изменения')

class ServiceAdd(FlaskForm):
    type = SelectField('Категория', choices=[('Категория не выбрана', '(Выберите категорию)'),
                                             ('Социально-бытовые', 'Социально-бытовые'),
                                             ('Социально-медицинские', 'Социально-медицинские'),
                                             ('Социально-психологические', 'Социально-психологические'),
                                             ('Социально-педагогические', 'Социально-педагогические'),
                                             ('Социально-правовые', 'Социально-правовые'),
                                             ('Услуги в целях повышения коммуникативного потенциала получателей социальных услуг, имеющих ограничения жизнидеятельности, в том числе детей-инвалидов', 'Услуги в целях повышения коммуникативного потенциала'),
                                             ('Социально-трудовые', 'Социально-трудовые'),
                                             ('Срочные услуги', 'Срочные услуги')], render_kw={'class': 'form-control'})
    name = StringField('Название услуги', validators=[DataRequired(), Length(min=2, max=250)])
    price = StringField('Цена', validators=[DataRequired(), Length(min=2, max=250)])
    submit = SubmitField('Добавить')

class ServiceEdit(FlaskForm):
    type = SelectField('Категория', choices=[('Категория не выбрана', '(Выберите категорию)'),
                                             ('Социально-бытовые', 'Социально-бытовые'),
                                             ('Социально-медицинские', 'Социально-медицинские'),
                                             ('Социально-психологические', 'Социально-психологические'),
                                             ('Социально-педагогические', 'Социально-педагогические'),
                                             ('Социально-правовые', 'Социально-правовые'),
                                             ('Услуги в целях повышения коммуникативного потенциала получателей социальных услуг, имеющих ограничения жизнидеятельности, в том числе детей-инвалидов', 'Услуги в целях повышения коммуникативного потенциала'),
                                             ('Социально-трудовые', 'Социально-трудовые'),
                                             ('Срочные услуги', 'Срочные услуги')], render_kw={'class': 'form-control'})
    name = StringField('Название услуги', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    submit = SubmitField('Сохранить изменения')


class ServiceReportForm(FlaskForm):
    report_type = SelectField('Тип отчета',
                            choices=[('monthly', 'Ежемесячный'),
                                    ('client', 'По клиенту')],
                            render_kw={'class': 'form-control'})
    month = StringField('Месяц', render_kw={'type': 'month', 'class': 'form-control'})
    client_id = SelectField('Клиент',
                          choices=[],
                          render_kw={'class': 'form-control'})
    submit = SubmitField('Сформировать отчет')
