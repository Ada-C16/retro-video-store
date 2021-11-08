from app import db
from datetime import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    postal_code = db.Column(db.String(10)) # Up to 10 chars in case using extended postal code
    registered_at = db.Column(db.DateTime)
    phone = db.Column(db.String(30))
    __tablename__ = "customers"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "postal_code": self.postal_code,
            "registered_at": self.registered_at.strftime("%a, %d %b %Y %I %z") if self.registered_at else None
        }

    @classmethod
    def from_json(cls, request_body):
        return cls(
            name = request_body["name"],
            postal_code = request_body["postal_code"],
            phone = request_body["phone"],
            registered_at = datetime.now()
        )

    @classmethod
    def validate_id(cls, id):
        try:
            int(id)
        except ValueError:
            return "", 400

        obj = cls.query.get(id)

        if not obj:
            return {
                "message": f"Customer {id} was not found"
            }, 404

    @classmethod
    def check_input_fields(cls, request_body):

        required_fields = ["name", "postal_code", "phone"]

        for field in required_fields:
            if field not in request_body or not isinstance(request_body[field], str):
                return { "details" : f"Request body must include {field}"}, 400
