from app import db

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.Date)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    rentals = db.relationship("Rental", backref="customer", lazy="dynamic")
    
    def to_dict(self):
        return{
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone
        }

    def get_rentals_count(self):
        return self.rentals.count()