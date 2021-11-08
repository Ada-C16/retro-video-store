from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    postal_code = db.Column(db.Integer)
    registered_at = db.Column(db.DateTime)
    phone = db.Column(db.String(30))
    __tablename__ = "customers"

    def to_dict(self):
        pass