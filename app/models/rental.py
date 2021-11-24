from app import db
from datetime import timedelta, date
from flask import abort, make_response
from app.models.video import Video
from app.models.customer import Customer


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    customer = db.relationship("Customer", backref="rentals", lazy="subquery")
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"))
    video = db.relationship("Video", backref="rentals", lazy="subquery")
    due_date = db.Column(db.DateTime, default=date.today() + timedelta(days=7))

    def rental_dict(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": len(self.customer.rentals),
            "available_inventory": self.video.total_inventory - len(self.video.rentals),
        }

    def customer_rentals_dict(self):
        return {
            "release_date": self.video.release_date,
            "title": self.video.title,
            "due_date": self.due_date,
        }

    def rental_customers_dict(self):

        return {
            "due_date": self.due_date,
            "name": self.customer.name,
            "phone": self.customer.phone,
            "postal_code": self.customer.postal_code,
        }

    @classmethod
    def rental_lookup(cls, video_id, customer_id):

        rental = cls.query.filter(
            video_id == video_id, customer_id == customer_id
        ).first()

        if not rental:
            abort(
                make_response(
                    {
                        "message": f"No outstanding rentals for customer {customer_id} and video {video_id}"
                    },
                    400,
                )
            )
        return rental

    @classmethod
    def check_out(cls, video_id, customer_id):

        video = Video.query.get(video_id)
        video.check_inventory()

        new_rental = cls(customer_id=customer_id, video_id=video_id)
        db.session.add(new_rental)
        db.session.commit()

        return new_rental

    @classmethod
    def check_in(cls, video_id, customer_id):

        rental = cls.rental_lookup(video_id, customer_id)
        db.session.delete(rental)
        db.session.commit()

        return rental
