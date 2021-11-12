from app import db
from flask import abort, make_response
from datetime import datetime, timezone


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    videos = db.relationship("Rental", back_populates="customer")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone
        }

    def update(self, customer_dict):
        self.validate_input(customer_dict)
        self.name = customer_dict["name"]
        self.postal_code = customer_dict["postal_code"]
        self.phone = customer_dict["phone"]
        return self

    def get_rentals(self):
        rentals = []
        for rental in self.videos:
            rental_dict = {
                "release_date": rental.video.release_date,
                "title": rental.video.title,
                "due_date": rental.due_date
            }
            rentals.append(rental_dict)
        return rentals

    def delete(self):
        if self.videos:
            for rental in self.videos:
                db.session.delete(rental)
        db.session.delete(self)

    @classmethod
    def validate_input(cls, customer_dict):
        if "name" not in customer_dict:
            abort(make_response(
                {"details": "Request body must include name."}, 400))
        if "postal_code" not in customer_dict:
            abort(make_response(
                {"details": "Request body must include postal_code."}, 400))
        if "phone" not in customer_dict:
            abort(make_response(
                {"details": "Request body must include phone."}, 400))

    @classmethod
    def new_from_dict(cls, customer_dict):
        "This method creates a new customer object from a dictionary of attributes"

        cls.validate_input(customer_dict)

        return cls(
            name=customer_dict["name"],
            postal_code=customer_dict["postal_code"],
            phone=customer_dict["phone"],
            registered_at=datetime.now(timezone.utc)
        )

    @classmethod
    def get_by_id(cls, id):
        try:
            int(id)
        except ValueError:
            abort(400)

        customer = cls.query.get(id)
        if not customer:
            abort(make_response(
                {"message": f"Customer {id} was not found"}, 404))

        return customer
