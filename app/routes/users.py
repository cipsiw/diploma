import bcrypt
from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_user, logout_user
#from ..functions import save_scan
from ..extensions import db, bcrypt
from ..models.users import Users
from ..forms import RegistrationForm, LoginForm

users = Blueprint('user', __name__)

@users.route('/user/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.passw.data).decode('utf-8')
        #scan_filename = save_scan(form.scans.data)
        user = Users(name=form.name.data, sec_name=form.sec_name.data, otch=form.otch.data, login=form.login.data, passw=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Вы успешно зарегистрировались","success")
            return redirect(url_for('user.login'))
        except Exception as e:
            print(str(e))
            flash(f"Ошибка регистрации","danger")
    return render_template('users/register.html', form=form)

@users.route('/user/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.passw, form.passw.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"Вы успешно авторизовались", "success")
            return redirect(next_page) if next_page else redirect(url_for('applic.all'))
        else:
            flash(f"Ошибка входа. Пожалуйста проверьте логин и пароль", "danger")
    return render_template('users/login.html', form=form)

@users.route('/user/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    flash(f"Вы вышли из учетной записи", "success")
    return redirect(url_for('applic.all'))