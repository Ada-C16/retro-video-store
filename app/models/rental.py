from app import db
import datetime
from sqlalchemy.orm import backref


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow() + datetime.timedelta(days=7))
    checked_out = db.Column(db.Boolean)
    video = db.relationship("Video", backref=backref("rentals", cascade="delete"))
    customer = db.relationship("Customer", backref=backref("rentals", cascade="delete"))



    