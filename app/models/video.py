from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement= True, nullable=False)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer, nullable=True)
    customers = db.relationship("Customer", secondary="rental", backref="videos")
    rentals = db.relationship("Rental", backref="video", lazy=True)

    def to_dict(self):
        return {"id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory}

    def video_rentals(self):
        rentals = []
        for rental in self.rentals:
            rentals.append({
                "name": rental.customer.name,
                "phone": rental.customer.phone,
                "postal_code": rental.customer.postal_code,
                "due_date": rental.due_date
            })
        return rentals