from app import db
from datetime import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    postcode = db.Column(db.Integer)
    register_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        new_dict = {
            "name": self.name,
            "phone": self.phone,
            "postcode": self.postcode
        }
        
        return new_dict