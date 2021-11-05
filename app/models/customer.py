from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    register_at = db.Column(db.DateTime) 
    # videos = db.relationship("Video", backref="customer", lazy=True)

# reason for str = many zip codes start with a zero; if you store as int you will lose leading zero

    def to_json(self, postal_code=None, phone_number=None):
        return {
            "id" : self.id,
            "name" : self.name,
            "postal_code" : self.postal_code,
            "phone_number" : self.phone_number,
            "register_at" : self.register_at
        }
