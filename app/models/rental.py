from app import db
from datetime import timedelta
from sqlalchemy.sql import func
from app.models.customer import Customer
from app.models.video import Video

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete='cascade'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id', ondelete='cascade'))
    check_out_time = db.Column(db.DateTime, server_default=func.now())
    # videos_checked_out_count = customer rentals
    # available_inventory = video.total_inventory - customer rentals
    # + timedelta(days=7)
    
    def create_dict(self):
        customer = Customer.query.filter_by(id=self.customer_id).first()
        out_count = Rental.query.filter_by(video_id = self.video_id).count()
        total_count = Video.query.get(self.video_id).total_inventory
        return_dict = {
            "rental_id":self.rental_id,
            "customer_id":self.customer_id,
            "video_id":self.video_id,
            "name": customer.id,
            "due_date": self.check_out_time + timedelta(days=7),
            "videos_checked_out_count" : out_count,
            "available_inventory": total_count - out_count
            }
        return return_dict