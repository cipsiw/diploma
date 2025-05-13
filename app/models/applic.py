from ..extensions import db
from datetime import datetime

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(250))
    service = db.Column(db.String(250))
    stuff = db.Column(db.String(250))
    date = db.Column(db.DateTime, default=datetime.utcnow)
