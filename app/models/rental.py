from app import db
from datetime import datetime, timedelta
from .video import Video

class Rental(db.Model):
    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True, nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.video_id'), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime)
    checked_out = db.Column(db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "checked_out": self.checked_out,
            "due_date": self.due_date.strftime("%Y-%m-%d") if self.due_date else None,
        }

    def to_dict_check_out(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date.strftime("%Y-%m-%d") if self.due_date else None,
            "videos_checked_out_count": Rental.get_customer_number_videos_checked_out(self.customer_id),
            "available_inventory": Rental.get_available_video_inventory(self.video_id)
        }
    def to_dict_check_in(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "videos_checked_out_count": Rental.get_customer_number_videos(self.customer_id),
            "available_inventory": Rental.get_available_video_inventory(self.video_id)
        }

    @classmethod
    def from_json(cls, customer_id, video_id):

        now = datetime.now()

        new_rental = cls(
            customer_id = customer_id,
            video_id = video_id,
            checked_out = True,
            due_date = now + timedelta(days=7)
        )

        return new_rental

    @staticmethod
    def get_available_video_inventory(video_id):

        video = Video.query.get(video_id)
        total_inventory = video.total_inventory

        rentals = Rental.query.filter_by(video_id = video_id, checked_out = True).count()

        available_inventory = total_inventory - rentals

        return available_inventory

    @staticmethod
    def get_customer_number_videos_checked_out(customer_id):
        
        videos = Rental.query.filter_by(customer_id = customer_id).count()

        return videos

    @staticmethod
    def get_customer_number_videos(customer_id):
        
        videos = Rental.query.filter_by(checked_out = True).count()

        return videos
