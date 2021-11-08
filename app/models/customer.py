from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    postal_code=db.Column(db.Integer)
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
   
