from app import db
from .video import Video 
from .customer import Customer
import datetime

class Rental(db.Model):
    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key =True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False) 
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False) 
    due_date = db.Column(db.DateTime, nullable=False)

 #finds the number of videos that are checked out from that video id
    def find_rentals(self, video_id):   
        count= 0
        rentals = Rental.query.all()
        for rental in rentals:
            if rental.video_id == video_id:
                count += 1
        return count

    def get_available_inventory(self):
        rental = Video.query.get(self.video_id)
        return rental.total_inventory - self.find_rentals(rental.id)

    # we need the video id of the rental and get the inventory attribute of that
    # minus find_rentals with video id  

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "videos_checked_out_count": self.find_rentals(self.video_id),
            "available_inventory": self.get_available_inventory(),
        }

    def get_rental_by_customer(self, id):
        video = Video.query.get(id)

        return {
            "release_date": video.release_date,
            "title": video.title,
            "due_date": self.due_date
        }

    def get_rental_by_video(self, id):
        customer = Customer.query.get(id)

        return {
            "due_date": self.due_date,
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code
        }

def due_date():
    return datetime.datetime.now() + datetime.timedelta(days=7)