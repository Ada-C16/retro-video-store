from app import db
from datetime import timedelta, date
from datetime import datetime, timedelta


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id", ondelete="CASCADE"), nullable=False, )
    video_id = db.Column(db.Integer, db.ForeignKey("video.id",ondelete="CASCADE"), nullable=False, )
    due_date = db.Column(db.DateTime)
    checked_out = db.Column(db.Boolean, default=False)
    video = db.relationship("Video", backref="video_rentals")  # added into the video class by having the relationship setup
    customer = db.relationship("Customer", backref="customer_rentals")  # add an attribute.


# composite Key?
