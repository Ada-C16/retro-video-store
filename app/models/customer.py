from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    rentals = db.relationship("Rental", backref="customers")
    # video = db.relationship("Video", backref="customers")
