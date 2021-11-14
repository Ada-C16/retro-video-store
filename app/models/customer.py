from flask import current_app
from app import db


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    customer_registration = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)

    def customer_information(self):
        return {
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.customer_registration,
            "postal_code": self.postal_code,
            "phone": self.phone,
        }
