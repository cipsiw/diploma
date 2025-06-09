import bcrypt
from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_user, logout_user, login_required
#from ..functions import save_scan
from ..extensions import db, bcrypt
from ..models.users import Users
from ..forms import RegistrationForm, LoginForm, UserEdit

from flask import send_file
from io import BytesIO
import pandas as pd
from datetime import datetime

users = Blueprint('user', __name__)

@users.route('/user/all', methods=['POST', 'GET'])
@login_required
def all():
    user = Users.query.order_by(Users.id).all()
    return render_template('users/all.html', users=user)

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

@users.route('/user/add', methods=['POST', 'GET'])
def adding():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.passw.data).decode('utf-8')
        #scan_filename = save_scan(form.scans.data)
        user = Users(name=form.name.data, sec_name=form.sec_name.data, otch=form.otch.data, login=form.login.data, passw=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Новый пользователь добавлен","success")
        except Exception as e:
            print(str(e))
            flash(f"Ошибка добавления","danger")
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

@users.route('/user/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update(id):
    user = Users.query.get_or_404(id)
    form = UserEdit(obj=user)
    form.role.data = user.status

    if form.validate_on_submit():
        try:
            user.login = form.login.data
            user.sec_name = form.sec_name.data
            user.name = form.name.data
            user.otch = form.otch.data
            user.status = form.role.data
            if form.passw.data:
                user.passw = bcrypt.generate_password_hash(form.passw.data).decode('utf-8')
            db.session.commit()
            flash("Изменения сохранены", "success")
            return redirect(url_for('user.all'))
        except Exception as e:
            db.session.rollback()
            flash(f"Ошибка при обновлении: {str(e)}", "danger")
            print(f"Ошибка: {str(e)}")

    return render_template('users/user_update.html', form=form, user=user)

@users.route('/user/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete(id):
    user = Users.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash("Пользователь успешно удален", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Ошибка при удалении: {str(e)}", "danger")
    return redirect(url_for('user.all'))

