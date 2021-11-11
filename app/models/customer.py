from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime, nullable = True)
    rentals = db.relationship('Rental', backref = 'customer', lazy = True)

    def customer_dict(self):
        return{
        "id": self.id,
        "name": self.name,
        "postal_code": self.postal_code,
        "phone": self.phone,
        "register_at": self.register_at
        }