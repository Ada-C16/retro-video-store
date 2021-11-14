from app import db
from sqlalchemy.orm import backref

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True, nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True, nullable=False)
    checked_in= db.Column(db.Boolean)
    due_date = db.Column(db.DateTime, nullable=True)
# this relationship establishes a new attribute for each rental object, which allows it to access the Video object
    video =db.relationship('Video', backref='rentals')
