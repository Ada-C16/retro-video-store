from app import db
from flask import abort, make_response
from datetime import datetime, timezone

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    postal_code=db.Column(db.String)
    phone=db.Column(db.String)
    registered_at=db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone
        }

    @classmethod
    def new_from_dict(cls, customer_dict):
        "This method creates a new customer object from a dictionary of attributes"


        if "name" not in customer_dict:
            abort(make_response({"details": "Request body must include name."}, 400))
        if "postal_code" not in customer_dict:
            abort(make_response({"details": "Request body must include postal_code."}, 400))
        if "phone" not in customer_dict:
            abort(make_response({"details": "Request body must include phone."}, 400))
        
        return cls(
            name=customer_dict["name"],
            postal_code=customer_dict["postal_code"],
            phone=customer_dict["phone"],
            registered_at=datetime.now(timezone.utc)
        )

    @classmethod
    def get_by_id(cls, id):
        try:
            int(id)
        except ValueError:
            abort(400)

        customer = cls.query.get(id)
        if not customer:
            abort(make_response({"message": f"Customer {id} was not found"}, 404))
            
        return customer



