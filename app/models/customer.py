from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    postal_code = db.Column(db.Integer)
    phone_number = db.Column(db.String(15))
    register_at = db.Column(db.DateTime)
