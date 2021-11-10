from app import db
from datetime import date


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime, default= date.today())
    videos = db.relationship("Video", secondary="rental", backref="customers")

    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "register_at": self.register_at
        }
