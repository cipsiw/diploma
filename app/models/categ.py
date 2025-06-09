from ..extensions import db
class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(250))
    cat_reqs = db.Column(db.String(250))


