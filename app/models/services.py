from ..extensions import db
class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(250))
    name = db.Column(db.String(250))
    price = db.Column(db.String(250))
