from app import db
from app.models.customer import Customer
from app.models.video import Video
import datetime as dt

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    customer = db.Column('customer_id', db.Integer, db.ForeignKey('customer.id', ondelete = 'cascade'))
    video = db.Column('video_id', db.Integer, db.ForeignKey('video.id', ondelete = 'cascade'))
    checkout_date = db.Column(db.DateTime, default = dt.datetime.now())
    due_date = db.Column(db.DateTime, default = dt.datetime.now() + dt.timedelta(days = 7))
    videos_checked_out_count = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)
    checked_in = db.Column(db.Boolean)

    def to_json(self):
        return {
            "customer_id": self.customer, 
            "video_id": self.video, 
            "videos_checked_out_count": self.videos_checked_out_count,
            "available_inventory": self.available_inventory
        }

def query_customers_videos(customer_id):
    videos = Video.query.join(Rental).join(Customer).filter(Customer.id == customer_id, Rental.checked_in == False).all()
    return videos
    
def count_a_videos_inventory(video_id, video_inventory):
    checked_out = Video.query.join(Rental).filter(Video.id == video_id, Rental.checked_in == False).all()
    return video_inventory - len(checked_out)

def customer_history(customer_id):
    rentals = Rental.query.join(Customer).join(Video).filter(Customer.id == customer_id).add_columns(Video.title, Rental.checkout_date, Rental.due_date).all()
    rental_history = []
    for rental in rentals:
        rental_history.append({
            "title": rental.title,
            "checkout_date": rental.checkout_date,
            "due_date": rental.due_date
        })
    return rental_history