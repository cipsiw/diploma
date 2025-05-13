from flask import Blueprint, render_template, request, redirect, flash, abort
from flask_login import login_required, current_user

from ..models.users import Users
from ..forms import StuffForm
from ..extensions import db
from ..models.applic import Request

applic = Blueprint('applic', __name__)

@applic.route('/', methods=['POST', 'GET'])
def all():
    applics = Request.query.order_by(Request.date.desc()).all()
    return render_template('applic/all.html', applics=applics, user=Users)

@applic.route('/applic/create', methods=['POST', 'GET'])
@login_required
def create():
    form = StuffForm()
    form.stuff.choices = [s.name for s in Users.query.filter_by(status='admin').all()]
    if request.method == 'POST':

        service = request.form.get('service')
        stuff = request.form.get('stuff')

        stuff_id = Users.query.filter_by(name=stuff).first().id

        applic = Request(client=current_user.id, service=service, stuff=stuff_id)

        print(applic.client)

        try:
            db.session.add(applic)
            db.session.commit()
            flash(f"Заявка была создана", "success")
            return redirect('/')
        except Exception as e:
            print(str(e))

    else:
        return render_template('applic/create.html', form=form)

@applic.route('/applic/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update(id):
    applic = Request.query.get(id)
    if applic.user.id == current_user.id:
        if request.method == 'POST':

            applic.client = request.form.get('client')
            applic.service = request.form.get('service')
            applic.stuff = request.form.get('stuff')

            try:
                db.session.commit()
                flash(f"Заявка была отредактирована", "success")
                return redirect('/')
            except Exception as e:
                print(str(e))
        else:
            return render_template('applic/update.html', applic=applic)
    else:
        abort(403)

@applic.route('/applic/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete(id):
    applic = Request.query.get(id)
    if applic.user.id == current_user.id:
        try:
            db.session.delete(applic)
            db.session.commit()
            flash(f"Заявка была удалена", "success")
            return redirect('/')
        except Exception as e:
            print(str(e))
            return str(e)