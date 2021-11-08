from app import db

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone_number = db.Column(db.String)
    registration_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.registration_at,
            "postal_code": self.postal_code,
            "phone": self.phone_number
        }