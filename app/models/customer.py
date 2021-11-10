from sqlalchemy.orm import backref
from app import db
from os import register_at_fork
from datetime import datetime

class Customer(db.Model):
    __tablename__ = "customers"
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow())
    
    videos_checked_out_count = db.Column(db.Integer, default = 0, nullable = True)
    rentals = db.relationship('Rental',backref='customers', lazy=True)

    def to_dict(self):
        result = {
            "id":self.customer_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone":self.phone,
            "registered_at": self.registered_at,
            "videos_checked_out_count": self.videos_checked_out_count
        }
        # if self.rentals:
        #     result["rentals"]=self.rentals
        return result