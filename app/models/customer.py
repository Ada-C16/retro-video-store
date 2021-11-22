from sqlalchemy.orm import backref
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime)
    videos = db.relationship("Video", secondary="rentals", backref="customers")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": self.register_at,
            "postal_code": self.postal_code,
            "phone": self.phone
        }