from app import db
from datetime import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    postal_code = db.Column(db.String)
    register_at = db.Column(db.DateTime, default=datetime.now)
    rental = db.relationship('Rental', backref='customer', lazy=True)

    def to_dict(self):
        new_dict = {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "postal_code": self.postal_code,
            "register_at": self.register_at,
        }
        
        return new_dict