from app import db
from datetime import datetime, timezone, timedelta
from app.models.video import Video
from flask import current_app

class Rental(db.Model):
    __tablename__ = 'rental'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True, nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime)
    # videos_checked_out_count = db.Column(db.Integer)
    # available_inventory = db.Column(db.Integer)

    def to_json(self):
        rental_dict = {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": db.session.query(Rental).filter(Rental.customer_id == self.customer_id).count(),
            "available_inventory": Video.query.get(self.video_id).total_inventory - db.session.query(Rental).filter(Rental.video_id == self.video_id).count()    
            # "videos_checked_out_count": cls.calc_videos_checked_out(self.customer_id),
            # "available_inventory": cls.calc_available_inventory(self.video_id)
        }
        return rental_dict


    @classmethod
    def from_json(cls, request_body):
        return cls(
            customer_id=request_body["customer_id"],
            video_id=request_body["video_id"],
            due_date=datetime.now(timezone.utc) + timedelta(days=7),
            # videos_checked_out_count =request_body["videos_checked_out_count"],
            # available_inventory=request_body["available_inventory"]
            )

    @classmethod
    def calc_videos_checked_out(cls, customer_id):
        videos_checked_out_count = db.session.query(Rental).filter(Rental.customer_id == customer_id).count()
        return videos_checked_out_count
    
    @classmethod
    def calc_available_inventory(cls, video_id):
        video = Video.query.get(video_id)
        available_inventory = video.total_inventory - db.session.query(Rental).filter(Rental.video_id == video_id).count()
        # video = db.session.query(Video).filter(id=video_id)


        return available_inventory            