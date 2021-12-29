from app import db

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True,nullable=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), primary_key=True,nullable=True)
    due_date = db.Column(db.DateTime)
    videos_checked_out_count = db.Column(db.Integer)
    available_inventory =  db.Column(db.Integer)
    videos_checked_in = db.Column(db.Boolean, default=False)


 
