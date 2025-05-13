from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import  LoginManager

login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()
db = SQLAlchemy()
