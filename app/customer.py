from flask import current_app
from app import db


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String)
    customer_registration = db.Column(db.String)
    postal_code = db.Column(db.Smallint)
    customer_number = db.Column(db.String)

    def customer_information(self):
        return {
            "id": 1,
            "name": "Shelley Rocha",
            "registered_at": "Wed, 29 Apr 2015 07:54:14 -0700",
            "postal_code": 24309,
            "phone": "(322) 510-8695",
        }
