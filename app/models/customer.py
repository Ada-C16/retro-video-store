from app import db

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    registered_at = db.Column(db.DateTime)

    def customer_dict(self):
        return {
        "id": self.customer_id,
        "name": self.name,
        "phone": self.phone,
        "postal_code": self.postal_code,
        "registered_at": self.registered_at
    }