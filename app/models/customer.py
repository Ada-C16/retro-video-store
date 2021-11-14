from flask import current_app
from app import db
from app.models.rental import Rental

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)
    videos = db.relationship('Video', secondary='rentals', backref='customers')
    
    def to_dict(self):
        '''takes instance of Customer and returns a formatted dictionary
        that includes instance attributes as key, value pairs'''
        customer_dict = {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at,
            }
        
        return customer_dict


