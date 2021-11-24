from app import db

class Rental(db.Model):
    __tablename__ = 'rentals'
    
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    is_checked_in = db.Column(db.Boolean, default=False, nullable=False)
