from app import db

class Rental(db.Model):
    __tablename__ = 'rentals'
    
    # video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True, nullable=False)
    # # customer_id = db.Column(db.Integer, db.ForeignKey('customer_id'), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime)
    # videos_checked_out_count = db.Column(db.Integer) 
    # available_inventory = db.Column(db.Integer) 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True, nullable=False)
    is_checked_in = db.Column(db.Boolean, default=False, nullable=False)
