from app import db

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable = True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), nullable = True)
