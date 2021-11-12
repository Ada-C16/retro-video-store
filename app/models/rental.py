from app import db
from flask import current_app
from sqlalchemy.orm import backref
from datetime import datetime, timedelta, date, time
from app.models.video import Video

from app.models.customer import Customer

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime)
    video = db.relationship("Video", back_populates="rentals")
    customer= db.relationship("Customer", back_populates="rentals")

    @staticmethod
    def generate_due_date():
        rental_window = timedelta(days=+7)
        now = date.today()
        due_date = now + rental_window
        return due_date
    
    # def get_available_inventory(self,video_id):
    #     video = Video.get.query(video_id)
    #     count = Rental.query.filter_by(video_id).count()
    #     return video.total_inventory() - count

    def to_dict(self):
        return {
            "id" : self.id, 
            "customer_id" : self.customer_id,
            "video_id" : self.video.id, 
            "due_date" : self.due_date,
            "videos_checked_out_count":self.customer.video_checked_out(),
            "available_inventory": self.video.remaining_videos()
        }
