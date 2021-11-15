from app import db

class Customer(db.Model):
    __tablename__ = "customers_table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    videos = db.relationship("Video", secondary="rentals_table", backref="customers_table")
