from sqlalchemy.orm import backref
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)   
    register_at = db.Column(db.DateTime)
    videos = db.relationship("Rental", backref="Customer", cascade="all, \
        delete-orphan", lazy="joined")

    def to_json(self):
        res = {
            "id" : self.id,
            "name" : self.name,
            "registered_at" : self.register_at,
            "postal_code" : self.postal_code,
            "phone" : self.phone_number
        }
        return res

    # def from_json(cls):
    #     pass

    # def append_to_list(self, customers_json):
    #     return [customer for customer in customers_json]