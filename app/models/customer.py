from flask import current_app
from app import db

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)


    def to_dict(self):
        customer_dict = {
            "id": self.customer_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at,
            }
        # example for how the conditional to change the form of the dictionary is
        # if self.goal_id is not None:
        #     task_dict["goal_id"] = self.goal_id
        
        return customer_dict