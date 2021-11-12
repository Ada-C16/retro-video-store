from flask import current_app
from sqlalchemy.orm import backref
from app import db
from datetime import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime)
    #videos_checked_out = db.Column(db.Integer, default=0)
    rentals = db.relationship("Rental", back_populates= "customer") #NEW
    
    def to_dict(self): 
        return {
            "id": self.id,
            "name": self.name,
            "postal_code" : self.postal_code,
            "phone" : self.phone,
            "register_at" : self.register_at,
        }
    
    def video_checked_out(self):
        return len(self.rentals)