from app import db

# join table 
class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    due_date = db.Column(db.DateTime())
    videos_checkout_count = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)
