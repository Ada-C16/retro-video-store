from app import db
from sqlalchemy.orm import backref


class Customer(db.Model):
    id = db.Column(db.Integer, autoincrement = True, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime)
    rentals = db.relationship("Rental")
    rented_videos = db.relationship("Video", secondary="rental")

    def to_dict(self):
        {
        "id": self.id,
        "name": self.name,
        "postal_code": self.postal_code,
        "phone": self.phone,
        "register_at": self.register_at,
        }

