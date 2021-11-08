from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.Integer, nullable=True)
    phone_num = db.Column(db.String, nullable=False)
    register_at = db.Column(db.DateTime, nullable=False)
