from app import db

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False) #not sure if nullable has to be false
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), nullable=False) #not sure if nullable has to be false
