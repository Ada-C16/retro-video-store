from app import db
from sqlalchemy.sql.functions import func
import datetime
from app.models.video import Video
from app.models.customer import Customer


class Rental(db.Model):
    # __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow() + datetime.timedelta(days=7))

    def rental_dict(self):
        video = Video.query.get(self.video_id)
        available_inventory = video.total_inventory - len(video.rentals)
        customer = Customer.query.get(self.customer_id)

        return {
            "video_id": self.video_id,
            "customer_id": self.customer_id,
            "videos_checked_out_count": customer.videos_checked_out,
            "available_inventory": available_inventory
        }

    @staticmethod
    def checkin_dict(customer, video):
        return {
            "video_id": video.id,
            "customer_id": customer.customer_id,
            "videos_checked_out_count": customer.videos_checked_out,
            "available_inventory": video.total_inventory + len(video.rentals)
        }
