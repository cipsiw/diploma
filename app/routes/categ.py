from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required
from ..extensions import db, bcrypt
from ..models.categ import Categories
from ..forms import CategAdd, CategEdit

category = Blueprint('categories', __name__)

@category.route('/categories/all', methods=['POST', 'GET'])
@login_required
def all():
    categories = Categories.query.order_by(Categories.id).all()
    return render_template('categ/all.html', categories=categories)

@category.route('/categories/add', methods=['POST', 'GET'])
@login_required
def add():
    form = CategAdd()
    if form.validate_on_submit():
        try:
            category = Categories(cat_name=form.name.data, cat_reqs=form.reqs.data)
            db.session.add(category)
            db.session.commit()
            flash("Категория успешно добавлена", "success")
            return redirect(url_for('categories.all'))
        except Exception as e:
            flash(f"Ошибка при добавлении: {str(e)}", "danger")
    return render_template('categ/create.html', form=form)

@category.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    category = Categories.query.get_or_404(id)
    form = CategEdit(obj=category)
    if form.validate_on_submit():
        try:
            category.cat_name = form.name.data
            category.cat_reqs = form.reqs.data
            db.session.commit()
            flash("Категория успешно обновлена", "success")
            return redirect(url_for('categories.all'))
        except Exception as e:
            db.session.rollback()
            flash(f"Ошибка при обновлении: {str(e)}", "danger")
    return render_template('categ/update.html', form=form, category=category)

@category.route('/categories/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete(id):
    category = Categories.query.get_or_404(id)
    try:
        db.session.delete(category)
        db.session.commit()
        flash("Услуга успешно удалена", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Ошибка при удалении: {str(e)}", "danger")
    return redirect(url_for('categories.all'))