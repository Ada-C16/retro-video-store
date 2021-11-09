from app import db
from sqlalchemy.sql.functions import func
import datetime


class Rental(db.Model):
    # __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.Integer, db.ForeignKey(
        'video.id'), primary_key=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.customer_id'), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.utcnow() + datetime.timedelta(days=7))
                    
    # customer = db.relationship("Customer", backref="rentals")
    # video = db.relationship("Video", backref="rentals")