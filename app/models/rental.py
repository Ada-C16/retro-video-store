from app import db

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable = True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable = True)
