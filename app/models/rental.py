from app import db


class Rental(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey(
        'video.id'), primary_key=True)
    due_date = db.Column(db.DateTime)
    customer = db.relationship("Customer", back_populates="videos")
    video = db.relationship("Video", back_populates="customers")
