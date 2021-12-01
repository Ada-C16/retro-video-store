from app import db
from datetime import date, datetime, timedelta

class Rental(db.Model):

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True,nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), primary_key=True,nullable=False)
    videos_checked_out_count = db.Column(db.Integer)
    rental_date = db.Column(db.Date)
    checked_in = db.Column(db.Boolean, nullable=True)
    
    def __init__(self, customer_id, video_id):
        self.customer_id = customer_id
        self.video_id = video_id
        self.videos_checked_out_count = 1
        self.rental_date = datetime.today()
        self.checked_in = False 

    def calculate_due_date(self):
        return  self.rental_date + timedelta(days=7)

    
