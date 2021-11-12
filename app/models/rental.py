from app import db
from datetime import datetime, timedelta
from app.models.video import Video

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime, default=(datetime.now() + timedelta(days=7)))
    checked_in = db.Column(db.Boolean, default=False)

    def to_dict(self, available_inv=None):
        # find num of videos checked out by customer
        num_checked_out = len(Rental.query.filter_by(customer_id=self.customer_id, checked_in=False).all())
        # calculate available inventory
        video = Video.query.get(self.video_id)
        total_inventory = int(video.total_inventory)
        total_checked_out = len(Rental.query.filter_by(video_id=self.video_id, checked_in=False).all())
        available_inv = total_inventory - total_checked_out

        return {
            'customer_id': self.customer_id,
            'video_id': self.video_id,
            'due_date': self.due_date,
            'videos_checked_out_count': num_checked_out,
            'available_inventory': available_inv
        }