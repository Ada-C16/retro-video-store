from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    register_at = db.Column(db.DateTime) 
    # videos = db.relationship("Video", backref="customer", lazy=True)

    def to_json(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "postal_code" : self.postal_code,
            "phone" : self.phone,
            "register_at" : self.register_at
        }

