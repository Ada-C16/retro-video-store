from app import db

class Rental(db.Model):
    __tablename__ = 'rentals'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True, nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True, nullable=False)
    due_date = db.Column(db.String, nullable=False)
    
# Variables that will be defined in the route queries
# Normalization
# videos_checked_out_count = db.Column(db.Integer)
# available_inventory = db.Column(db.Integer)



