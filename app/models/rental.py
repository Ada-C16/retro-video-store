from app import db
from datetime import timedelta, date
from datetime import datetime, timedelta


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(
        db.Integer, db.ForeignKey("customer.id"), primary_key=True, nullable=False
    )
    video_id = db.Column(
        db.Integer, db.ForeignKey("video.id"), primary_key=True, nullable=False
    )
    due_date = db.Column(db.DateTime)
    checked_out = db.Column(db.Boolean, default=False)
