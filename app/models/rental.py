from app import db
from datetime import timedelta, date
from flask import abort
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
