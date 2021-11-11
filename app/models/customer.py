from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone_number = db.Column(db.String)
    register_at = db.Column(db.DateTime, nullable=True)

    def to_json(self):
        return {
                "id": self.id,
                "name": self.name,
                "postal_code": self.postal_code,
                "phone_number": self.phone_number,
                "register_at": False if self.completed_at == None else True
                }