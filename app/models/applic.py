from ..extensions import db
from datetime import datetime

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    service = db.Column(db.Integer, db.ForeignKey('services.id', ondelete='CASCADE'))
    stuff = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(13), default='Запланирована')
    document_path = db.Column(db.String(255))
    review = db.Column(db.String(500))

class AssignmentCounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_assigned_index = db.Column(db.Integer, default=0)
