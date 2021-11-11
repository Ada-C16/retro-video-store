from app import db
from datetime import datetime, timedelta

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True,nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), primary_key=True,nullable=False)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow() + datetime.timedelta(days = 7))