from flask import Blueprint, render_template, redirect, flash, url_for, request, abort
from flask_login import login_required
from ..extensions import db
from ..models.services import Services
from ..forms import ServiceAdd, ServiceEdit

service = Blueprint('services', __name__)

@service.route('/services/all', methods=['POST', 'GET'])
@login_required
def all():
    services = Services.query.order_by(Services.id).all()
    return render_template('services/all.html', services=services)

@service.route('/services/add', methods=['POST', 'GET'])
@login_required
def add():
    form = ServiceAdd()
    if form.validate_on_submit():
        try:
            service = Services(type=form.type.data, name=form.name.data, price=form.price.data)
            db.session.add(service)
            db.session.commit()
            flash("Услуга успешно добавлена", "success")
            return redirect(url_for('services.all'))
        except Exception as e:
            db.session.rollback()
            flash(f"Ошибка при добавлении: {str(e)}", "danger")
            print("Ошибка:", str(e))
    return render_template('services/create.html', form=form)

@service.route('/services/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    service = Services.query.get_or_404(id)
    form = ServiceEdit(obj=service)

    if form.validate_on_submit():
        try:
            form.populate_obj(service)
            db.session.commit()
            flash("Услуга успешно обновлена", "success")
            return redirect(url_for('services.all'))
        except Exception as e:
            db.session.rollback()
            flash(f"Ошибка при обновлении: {str(e)}", "danger")
    return render_template('services/update.html', form=form, service=service)

@service.route('/services/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete(id):
    service = Services.query.get_or_404(id)
    try:
        db.session.delete(service)
        db.session.commit()
        flash("Услуга успешно удалена", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Ошибка при удалении: {str(e)}", "danger")
    return redirect(url_for('services.all'))