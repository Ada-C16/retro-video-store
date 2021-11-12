from app import db
from datetime import datetime, timedelta, date
from .video import Video
from .customer import Customer

class Rental(db.Model):

    sort_fields = ["due_date"]

    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True, nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.video_id'), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime(timezone=True))
    checked_out = db.Column(db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "customer_name": Customer.query.get(self.customer_id).name,
            "video_id": self.video_id,
            "video_title": Video.query.get(self.video_id).title,
            "checked_out": self.checked_out,
            "due_date": self.due_date.strftime("%Y-%m-%d"),
        }

    def to_dict_check_out(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date.strftime("%Y-%m-%d"),
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

    def to_dict_customer_rentals(self):

        video = Video.query.get(self.video_id)

        return {
            "release_date": video.release_date,
            "title": video.title,
            "due_date": self.due_date.strftime("%Y-%m-%d"),
        }

    @classmethod
    def from_json(cls, customer_id, video_id):

        new_rental = cls(
            customer_id = customer_id,
            video_id = video_id,
            checked_out = True,
            due_date = datetime.utcnow() + timedelta(days=7)
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
