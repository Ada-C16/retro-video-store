from app import db
from flask import current_app
from datetime import datetime


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime)
    required_fields = ["name", "phone", "postal_code"]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "register_at": self.register_at,
        }

    def update(self, request_body):
        for key, value in request_body.items():
            if key in Customer.__table__.columns.keys():
                setattr(self, key, value)

    def get_rentals(self):
        rentals = [rental.customer_rentals_dict() for rental in self.rentals]
        return rentals
