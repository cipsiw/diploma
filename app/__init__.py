from flask import Flask
from .extensions import db, migrate, login_manager
from .config import Config
from .routes.users import users
from .routes.applic import applic
from .routes.categ import category
from .routes.service import service
from .routes.report import reports

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

    app.register_blueprint(users)
    app.register_blueprint(applic)
    app.register_blueprint(category)
    app.register_blueprint(service)
    app.register_blueprint(reports)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Вы не можете получить доступ к данной странице. Сначала авторизируйтесь'
    login_manager.login_message_category = 'info'


    with app.app_context():
        db.create_all()

    return app