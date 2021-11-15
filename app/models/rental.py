from app import db
from datetime import timedelta
from sqlalchemy.sql import func

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete='cascade'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id', ondelete='cascade'))
    due_date = db.Column(db.DateTime, server_default=func.now())
    # videos_checked_out_count = customer rentals
    # available_inventory = video.total_inventory - customer rentals
    # + timedelta(days=7)