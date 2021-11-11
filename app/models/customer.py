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
    videos_checked_out = db.Column(db.Integer, default=0)
    
    def to_dict(self): 
        return {
            "id": self.id,
            "name": self.name,
            "postal_code" : self.postal_code,
            "phone" : self.phone,
            "register_at" : self.register_at,
        }
    
    def video_checked_out(self):
        #customer = Customer.get.query(customer_id)
        #count = Rental.query.filter_by(Rental.customer_id==c_id).count()
        #count = db.session.query(Rental).filter_by(Rental.customer_id==c_id).count
        self.videos_checked_out += 1
        return self.videos_checked_out