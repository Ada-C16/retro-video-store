from flask import current_app
from sqlalchemy.orm import backref
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime)

    videos_rented = db.relationship("Video", secondary="rental", backref="customer")
    rentals=db.relationship("Rental", backref="customer")
    


    def to_dict(self):
        response_body = {
            "id": self.id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone
        }

        return response_body

    def put_request_dict(self):
        response_body = {
            "name": f"Updated ${self.name}",
            "phone": f"Updated ${self.phone}",
            "postal_code": f"Updated ${self.postal_code}"
        }

        return response_body