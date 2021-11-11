from app import db
from datetime import datetime, timezone

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)

    def to_json(self):
        customer_dict = {
                "id": self.id,
                "name": self.name,
                "registered_at": self.registered_at,
                "postal_code": self.postal_code,
                "phone": self.phone   
            }
        return customer_dict
    
    @classmethod
    def from_json(cls, request_body):
        return cls(name=request_body["name"],
        registered_at=datetime.now(timezone.utc),
        postal_code=request_body["postal_code"],
        phone=request_body["phone"])