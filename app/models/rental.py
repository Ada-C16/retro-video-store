from app import db
import datetime as dt

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customers = db.Column('customer_id', db.Integer, db.ForeignKey('customer.id'))
    videos = db.Column('video_id', db.Integer, db.ForeignKey('video.id'))
    due_date = dt.datetime.now() + dt.timedelta(days = 7)
    # videos_checked_out_count = find all videos under a customer id 
    videos_checked_out_count = 0
    
    available_inventory = 0
    checked_in = db.Column(db.Boolean) ## check
    
    def count_a_customers_videos(self, customer_id):
        # search rentals for customer_id 
        # count them if checked_in = True
        # + 1 (for current)
        pass

    def count_a_videos_inventory(self, video_id):
        # available_inventory = video.total_inventory - # all current checked out videos of that id
        # search for active rentals with a specific id
        # find len
        pass
