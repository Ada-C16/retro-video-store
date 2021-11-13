from app import db
import datetime

class Rental(db.Model):
    __tablename__ = 'rentals'
    rental_id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime, default=datetime.datetime.now() + datetime.timedelta(days=7), nullable=False)
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.video_id'), nullable=False)
    
    def to_dict(self):
        return {
            'rental_id': self.rental_id,
            'due_date': self.due_date,
            'customer_id': self.customer_id,
            'video_id': self.video_id
        }