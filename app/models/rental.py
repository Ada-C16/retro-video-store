from app import db
from datetime import datetime, timedelta

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime, default=(datetime.now() + timedelta(days=7)))
    checked_in = db.Column(db.Boolean, default=False)
    # set up one to many relationship (one customer to many rentals)
    customer = db.relationship("Customer", back_populates="rentals")
    video = db.relationship("Video", back_populates="rentals")

    def to_dict(self, available_inv=None):

        return {
            'customer_id': self.customer_id,
            'video_id': self.video_id,
            'due_date': self.due_date,
            'videos_checked_out_count': len(self.customer.rentals),
            'available_inventory': self.video.total_inventory - len(self.video.rentals)
        }