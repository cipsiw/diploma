from flask import send_file
from io import BytesIO
import pandas as pd
import xlsxwriter
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from flask_login import login_required, current_user
from sqlalchemy.orm import aliased
from ..models.applic import Request
from ..models.users import Users
from ..models.services import Services
from ..forms import ServiceReportForm
from ..extensions import db

Users_stuff = aliased(Users)
reports = Blueprint('reports', __name__)


@reports.route('/reports', methods=['GET', 'POST'])
@login_required
def service_reports():
    form = ServiceReportForm()

    # Заполняем список клиентов
    clients = Users.query.filter_by(status='client').all()
    form.client_id.choices = [('', '(Выберите клиента)')] + [(str(c.id), f"{c.sec_name} {c.name}") for c in clients]

    if request.method == 'POST' and form.validate_on_submit():
        try:
            report_type = form.report_type.data
            client_id = form.client_id.data
            month = form.month.data

            # Создаем базовый запрос с явными алиасами
            Users_stuff = aliased(Users)
            query = db.session.query(
                Request.id,
                Users.sec_name.label('client_sec_name'),
                Users.name.label('client_name'),
                Services.name.label('service_name'),
                Services.type.label('service_type'),
                Services.price,
                Request.date,
                Users_stuff.sec_name.label('stuff_sec_name'),
                Users_stuff.name.label('stuff_name')
            ).select_from(Request) \
                .join(Users, Request.client == Users.id) \
                .join(Services, Request.service == Services.id) \
                .join(Users_stuff, Request.stuff == Users_stuff.id) \
                .filter(Request.status == 'Выполнена')

            # Применяем фильтры
            if report_type == 'monthly' and month:
                month_start = datetime.strptime(month, '%Y-%m')
                next_month = month_start.replace(day=28) + timedelta(days=4)
                month_end = next_month - timedelta(days=next_month.day)
                query = query.filter(Request.date.between(month_start, month_end))
            elif report_type == 'client' and client_id:
                query = query.filter(Request.client == client_id)

            requests = query.all()

            if not requests:
                flash("Нет данных для отчета с выбранными параметрами", "warning")
                return redirect(url_for('reports.service_reports'))

            # Создаем DataFrame для Excel
            data = []
            total_amount = 0  # Общая сумма

            for req in requests:
                try:
                    price = float(req.price) if req.price else 0
                except (ValueError, TypeError):
                    price = 0

                total_amount += price

                data.append({
                    'ID заявки': req.id,
                    'Клиент': f"{req.client_sec_name} {req.client_name}",
                    'Услуга': req.service_name,
                    'Категория': req.service_type,
                    'Стоимость': price,
                    'Дата выполнения': req.date.strftime('%Y-%m-%d'),
                    'Сотрудник': f"{req.stuff_sec_name} {req.stuff_name}"
                })

            df = pd.DataFrame(data)

            # Добавляем итоговую строку
            summary_row = {
                'ID заявки': 'ИТОГО:',
                'Клиент': f"Количество услуг: {len(requests)}",
                'Услуга': '',
                'Категория': '',
                'Стоимость': total_amount,
                'Дата выполнения': '',
                'Сотрудник': ''
            }

            # Конвертируем в DataFrame и объединяем с основными данными
            df_summary = pd.DataFrame([summary_row])
            df = pd.concat([df, df_summary], ignore_index=True)

            # Создаем Excel файл в памяти
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Отчет по услугам', index=False)

                # Получаем объекты workbook и worksheet
                workbook = writer.book
                worksheet = writer.sheets['Отчет по услугам']

                # Форматирование итоговой строки
                bold_format = workbook.add_format({'bold': True, 'bg_color': '#FFFF00'})

                # Применяем форматирование к итоговой строке
                worksheet.set_row(len(requests), cell_format=bold_format)

                # Автоматическая ширина колонок
                for idx, col in enumerate(df.columns):
                    max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.set_column(idx, idx, max_len)

            output.seek(0)

            # Формируем имя файла
            filename = f"services_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

            return send_file(
                output,
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        except Exception as e:
            flash(f"Ошибка при формировании отчета: {str(e)}", "danger")
            return redirect(url_for('reports.service_reports'))

    return render_template('reports/service_report.html', form=form)