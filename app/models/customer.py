from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    postcode = db.Column(db.Integer)
    register_at = db.Column(db.DateTime)

    def to_dict(self):
        new_dict = {
            "name": self.name,
            "phone": self.phone,
            "postcode": self.postcode
        }
        
        return new_dict