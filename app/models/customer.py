from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    register_at = db.Column(db.Datetime)

    def customer_dict(self):
        name = self.name
        postal_code = self.postal_code
        phone_number = self.phone_number
        register_at = self.register_at