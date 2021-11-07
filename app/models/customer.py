from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    postal_code = db.Column(db.String(10))
    phone_number = db.Column(db.String)
    register_at = db.Column(db.DateTime)
