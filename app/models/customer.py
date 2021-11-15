from flask import current_app
from app import db
from datetime import date
from flask import Blueprint, jsonify, request


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    customer_registration = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, default=date.today())
    videos = db.relationship("Video", secondary="rental", backref="customers")

    def customer_information(self):
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": self.customer_registration,
            "postal_code": self.postal_code,
            "phone": self.phone,
        }
