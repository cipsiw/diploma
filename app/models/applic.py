from ..extensions import db
from datetime import datetime

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    service = db.Column(db.String(250))
    stuff = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)
