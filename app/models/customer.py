from app import db
from flask import abort, make_response

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    postal_code=db.Column(db.String)
    phone=db.Column(db.Integer)
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
    def get_by_id(cls, id):
        try:
            int(id)
        except ValueError:
            abort(400)

        customer = cls.query.get(id)
        if not customer:
            abort(make_response({"message": f"Customer {id} was not found"}, 404))
            
        return customer



