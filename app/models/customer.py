from app import db
from flask import make_response

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime)

    def return_customer_info(self):
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone
        }
    
    def new_customer(self):
        return {
            "id": self.id
        }

    def update_customer(self):
        return {
            "name": f"{self.name}", 
            "phone": f"{self.phone}",
            "postal_code": f"{self.postal_code}"
        }

def find_customer(id):
    try:
        customer = Customer.query.get(id)
    except:
        return {
            "found": False, 
            "return": make_response("", 400)
        }
    if customer is None:
        return {
            "found": False,
            "return": make_response({"message": f"Customer {id} was not found"}, 404 )
        }
    return {
        "found": True, 
        "info": customer
    }