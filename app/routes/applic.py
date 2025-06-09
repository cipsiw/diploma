import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from ..models.users import Users
from ..models.services import Services
from ..forms import ListForm, RequestEditForm
from ..extensions import db
from ..models.applic import Request, AssignmentCounter

UPLOAD_FOLDER = 'app/static/uploads/documents'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}

applic = Blueprint('applic', __name__)

@applic.route('/', methods=['POST', 'GET'])
@login_required
def all():
    if current_user.is_authenticated:
        if current_user.status == 'admin':
            # Администратор видит все заявки
            applics = Request.query.order_by(Request.date.desc()).all()
        elif current_user.status == 'stuff':
            # Сотрудник видит только свои заявки
            applics = Request.query.filter_by(stuff=current_user.id).order_by(Request.date.desc()).all()
        elif current_user.status == 'client':
            # Клиент видит только свои заявки
            applics = Request.query.filter_by(client=current_user.id).order_by(Request.date.desc()).all()
    else:
        applics = []
    return render_template('applic/all.html', applics=applics, user=Users)

@applic.route('/applic/create', methods=['POST', 'GET'])
@login_required
def create():
    form = ListForm()

    # Получаем список сотрудников
    staff_members = Users.query.filter_by(status='stuff').all()
    form.stuff.choices = [('', '(Выберите сотрудника)')] + [
        (str(s.id), f"{s.sec_name} {s.name} {s.otch}" if s.otch else f"{s.sec_name} {s.name}")
        for s in staff_members
    ]

    form.service.choices = [('', '(Выберите услугу)')] + [(str(s.id), s.name) for s in Services.query.all()]

    if current_user.status in ['stuff', 'admin']:
        form.client.choices = [('', '(Выберите клиента)')] + [
            (str(c.id), f"{c.sec_name} {c.name} {c.otch}" if c.otch else f"{c.sec_name} {c.name}")
            for c in Users.query.filter_by(status='client').all()
        ]

    if request.method == 'POST':
        service_id = request.form.get('service')
        document = request.files.get('document')
        document_path = None

        # Определяем клиента
        if current_user.status == 'client':
            client_id = current_user.id
        else:
            client_id = request.form.get('client')

        # Определяем сотрудника
        if current_user.status == 'stuff':
            # Если заявку создает сотрудник - назначаем на себя
            stuff_id = current_user.id
        else:
            # Для клиентов и админов - используем алгоритм распределения
            staff_members = Users.query.filter_by(status='stuff').order_by(Users.id).all()
            if not staff_members:
                flash("Нет доступных сотрудников для назначения", "danger")
                return render_template('applic/create.html', form=form)

            # Получаем или создаем счетчик
            counter = AssignmentCounter.query.first()
            if not counter:
                counter = AssignmentCounter(last_assigned_index=0)
                db.session.add(counter)
                db.session.commit()

            # Вычисляем следующего сотрудника
            next_index = (counter.last_assigned_index + 1) % len(staff_members)
            stuff_id = staff_members[next_index].id

            # Обновляем счетчик
            counter.last_assigned_index = next_index
            db.session.commit()

        # Обработка документа
        if document and document.filename:
            if '.' in document.filename and document.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                filename = secure_filename(document.filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                document.save(filepath)
                document_path = filepath
            else:
                flash("Недопустимый тип файла", "danger")
                return render_template('applic/create.html', form=form)

        # Создаем заявку
        applic = Request(client=client_id, service=service_id, stuff=stuff_id, document_path=document_path)

        try:
            db.session.add(applic)
            db.session.commit()
            flash("Заявка успешно создана", "success")
            return redirect('/')
        except Exception as e:
            db.session.rollback()
            flash(f"Ошибка при создании заявки: {str(e)}", "danger")
            print(str(e))

    return render_template('applic/create.html', form=form)
@applic.route('/applic/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update(id):
    applic = Request.query.get(id)
    if not applic:
        abort(404)

    if current_user.status == 'stuff' and applic.stuff != current_user.id:
        abort(403)
    elif current_user.status == 'client' and applic.client != current_user.id:
        abort(403)

    form = RequestEditForm(
        client=str(applic.client),
        service=str(applic.service),
        stuff=str(applic.stuff),
        status=applic.status
)
    # Заполняем списки выбора
    form.client.choices = [(str(c.id), f"{c.sec_name} {c.name}") for c in Users.query.filter_by(status='client').all()]
    form.service.choices = [(str(s.id), s.name) for s in Services.query.all()]
    form.stuff.choices = [(str(s.id), f"{s.sec_name} {s.name}") for s in Users.query.filter_by(status='stuff').all()]

    if request.method == 'POST':
        # Обработка данных формы
        applic.client = request.form.get('client')
        applic.service = request.form.get('service')
        applic.stuff = request.form.get('stuff')
        applic.status = request.form.get('status')

        # Обработка документа
        if 'delete_document' in request.form and request.form['delete_document'] == 'y':
            if applic.document_path:
                try:
                    os.remove(applic.document_path)
                except Exception as e:
                    print(f"Ошибка удаления файла: {e}")
                applic.document_path = None

        document = request.files.get('document')
        if document and document.filename:
            # Удаляем старый документ если есть
            if applic.document_path and os.path.exists(applic.document_path):
                os.remove(applic.document_path)

            # Сохраняем новый документ
            filename = secure_filename(f"doc_{applic.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{document.filename}")
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            document.save(filepath)
            applic.document_path = filepath

        try:
            db.session.commit()
            flash("Заявка успешно обновлена", "success")
            return redirect(url_for('applic.all'))
        except Exception as e:
            db.session.rollback()
            flash(f"Ошибка при обновлении заявки: {str(e)}", "danger")

    return render_template('applic/update.html', form=form, applic=applic)

@applic.route('/applic/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete(id):
    applic = Request.query.get(id)
    if not applic:
        abort(404)

    if current_user.status == 'admin' or \
            (current_user.status == 'stuff' and applic.stuff == current_user.id) or \
            (current_user.status == 'client' and applic.client == current_user.id):
        try:
            db.session.delete(applic)
            db.session.commit()
            flash(f"Заявка была удалена", "success")
            return redirect('/')
        except Exception as e:
            print(str(e))
            return str(e)
    else:
        abort(403)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_document_url(document_path):
    if document_path:
        return url_for('static', filename=document_path.split('static/')[-1])
    return None