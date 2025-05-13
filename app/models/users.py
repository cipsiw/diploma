from .applic import Request
from ..extensions import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    applic = db.relationship(Request, backref='user')
    sec_name = db.Column(db.String(50))
    name = db.Column(db.String(50))
    otch = db.Column(db.String(50))
    login = db.Column(db.String(50))
    status = db.Column(db.String(50), default='admin')
    passw = db.Column(db.String(200))
    scan = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)

