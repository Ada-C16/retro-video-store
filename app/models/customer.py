from flask import current_app
from app import db

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)

    #we do not want an attirbute because it wouldn't allow us to track changes happening\
    #simultaneously and would be harder to update
    # videos_checked_out = db.relationship("Rental", backref="customer_id")

    def to_dict(self):
        customer_dict = {
            "id": self.customer_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at,
            }
        
        return customer_dict

    #instance method for videos_checked_out here
    #query rentals db for all instances connected to customer_id
    #sort by those currently checked_out
    #get length of list
    #return length of list