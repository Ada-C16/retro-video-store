from app import db
from datetime import timedelta, date
from flask import abort, make_response
from sqlalchemy import delete


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    customer = db.relationship("Customer", backref="rentals", lazy="subquery")

    video_id = db.Column(db.Integer, db.ForeignKey("video.id"))
    video = db.relationship("Video", backref="rentals", lazy="subquery")

    due_date = db.Column(db.DateTime, default=date.today() + timedelta(days=7))

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": len(self.customer.rentals),
            "available_inventory": self.video.total_inventory - len(self.video.rentals),
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
