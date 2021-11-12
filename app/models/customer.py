from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)

    def customer_details(self):
        return {
        "id": self.id,
        "name": self.name,
        "postal_code": self.postal_code,
        "phone": self.phone
        }