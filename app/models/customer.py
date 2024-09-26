from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    postal_code = db.Column(db.String)
    register_at = db.Column(db.DateTime)
    videos = db.relationship("video", secondary="rental", backref="customers")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone" : self.phone,
            "postal_code" : self.postal_code,
            "register_at" : self.register_at
        }