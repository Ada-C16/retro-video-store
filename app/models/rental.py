from app import db
import datetime


class Rental(db.Model):
    __tablename__ = "video_rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), primary_key=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow() + datetime.timedelta(days=7))


   