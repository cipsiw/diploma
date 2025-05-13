from ..extensions import db


class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String(250))
    service_name = db.Column(db.String(250))
    service_price = db.Column(db.String(250))
