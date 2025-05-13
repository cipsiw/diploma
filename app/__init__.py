from flask import Flask
from .extensions import db, migrate, login_manager
from .config import Config
from .routes.users import users
from .routes.applic import applic


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(users)
    app.register_blueprint(applic)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Вы не можете получить доступ к данной странице. Сначала авторизируйтесь'
    login_manager.login_message_category = 'info'


    with app.app_context():
        db.create_all()

    return app