from app import db
from app.models.rental import Rental

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    register_at = db.Column(db.DateTime, nullable=True)
    number_of_rentals = db.Column(db.Integer, nullable=True)
    rentals = db.relationship("Rental", backref="customer", lazy=True)

    def to_dict(self):
        self.videos
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.register_at
        }

    def customer_rentals(self):
        rentals = []
        for rental in self.rentals:
            rentals.append({
                "title": rental.video.title,
                "release_date": rental.video.release_date,
                "due_date": rental.due_date
            })
        return rentals



