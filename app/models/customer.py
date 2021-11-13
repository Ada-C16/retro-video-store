from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    
    rental = db.relationship("Rental",passive_deletes=True, backref="customers")
    video = db.relationship("Video", passive_deletes=True, secondary = "rental", backref="customers")
