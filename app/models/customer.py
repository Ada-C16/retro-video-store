from app import db
from sqlalchemy.orm import relationship

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(30))
    name = db.Column(db.String(60))
    # postal_code = db.Column(db.String(30))
    postal_code = db.Column(db.String(60))
    # phone = db.Column(db.String(15))
    phone = db.Column(db.String(60))
    register_at = db.Column(db.DateTime)
    videos = db.relationship('Video', secondary='rentals', backref='customers')


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "register_at": self.register_at
        }