from app import db
import datetime as dt
from app.models.customer import Customer
from app.models.video import Video

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column('customer_id', db.Integer, db.ForeignKey('customer.id'))
    video = db.Column('video_id', db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime) # dt.datetime.now() + dt.timedelta(days = 7)
    # videos_checked_out_count = find all videos under a customer id 
    videos_checked_out_count = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)
    checked_in = db.Column(db.Boolean)
    
    def count_a_customers_videos(self, customer_id):
        # search rentals for customer_id 
        rentals = Customer.query.join(Rental).filter_by(id == customer_id, Rental.checked_in == True).all()
        # count them if checked_in = True
        return len(rentals) 
        # + 1 (for current)
        

    def count_a_videos_inventory(self, video_id):
        # available_inventory = video.total_inventory - # all current checked out videos of that id
        active_rentals = Video.query.join(Rental).filter_by(id == video_id, Rental.checked_in == False).all() 
        num_active = len(active_rentals)
        return num_active 
        # find len
        
    
    def check_in_json(self):
        pass

    def check_out_json(self, customer_id, video_id):
        return {
            "customer_id": customer_id, 
            "video_id": video_id, 
            "videos_checked_out_count": count_a_customers_videos(customer_id) + 1,
            "available_inventory": count_a_videos_inventory(video_id) - 1
        }