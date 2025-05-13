from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models.applic import Request

applic = Blueprint('applic', __name__)

@applic.route('/', methods=['POST', 'GET'])
def all():
    applics = Request.query.order_by(Request.date.desc()).all()
    return render_template('applic/all.html', applics=applics)

@applic.route('/applic/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':

        service = request.form.get('service')
        stuff = request.form.get('stuff')

        applic = Request(client=current_user.id, service=service, stuff=stuff)

        print(applic.client)

        try:
            db.session.add(applic)
            db.session.commit()
            flash(f"Заявка была создана", "success")
            return redirect('/')
        except Exception as e:
            print(str(e))

    else:
        return render_template('applic/create.html')

@applic.route('/applic/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update(id):
    applic=Request.query.get(id)
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

@applic.route('/applic/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete(id):
    applic=Request.query.get(id)
    try:
        db.session.delete(applic)
        db.session.commit()
        flash(f"Заявка была удалена", "success")
        return redirect('/')
    except Exception as e:
        print(str(e))
        return str(e)