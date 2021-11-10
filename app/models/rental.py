from app import db
from datetime import timedelta

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True, nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime + timedelta(days=7))
    # videos_checked_out_count = customer rentals
    # available_inventory = video.total_inventory - customer rentals