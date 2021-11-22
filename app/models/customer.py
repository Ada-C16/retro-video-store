from app import db
from sqlalchemy.orm import backref


class Customer(db.Model):
    id = db.Column(db.Integer, autoincrement = True, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime)
    # videos = db.relationship("Video",secondary="customer_videos", backref="customers")
    # rentals = db.relationship('Rental', backref="customer_rentals", lazy=True)


    def to_dict(self):
        response={ 
        "id": self.id,
        "name": self.name,
        "postal_code": self.postal_code,
        "phone": self.phone,
        "register_at": self.register_at,
        }
        return response

