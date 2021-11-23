from app import db
from datetime import datetime 

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    register_at = db.Column(db.DateTime) 
    rentals = db.relationship("Rental", backref="customer", lazy=True) 

    def to_json(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "postal_code" : self.postal_code,
            "phone" : self.phone,
            "register_at" : self.register_at
        }

    def new_customer(self, request_data):
        return Customer(
                name=request_data["name"], 
                postal_code=request_data["postal_code"],
                phone=request_data["phone"],
                register_at = datetime.now()
            )
