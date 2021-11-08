from flask import current_app
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)


    def to_dict(self):
        # self.is_complete = False if not self.completed_at else True

        # self.is_complete

        customer_dict = {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.register_at,
            }
        # example for how the conditional to change the form of the dictionary is
        # if self.goal_id is not None:
        #     task_dict["goal_id"] = self.goal_id
        
        return customer_dict