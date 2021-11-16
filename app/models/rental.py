from app import db
from datetime import timedelta, date
from datetime import datetime, timedelta


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), nullable=False)
    due_date = db.Column(db.DateTime)
    checked_out = db.Column(db.Boolean, default=False)
    video = db.relationship("Video", backref="rentals")  # added into the video class by having the relationship setup
    customer = db.relationship("Customer", backref="rentals")  # add an attribute.


# composite Key?
