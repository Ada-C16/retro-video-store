from sqlalchemy.orm import backref
from app import db
from datetime import datetime, timedelta

def week_later():
    return datetime.utcnow() + timedelta(days=7)
    
class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete='cascade'),  nullable=True)
    customer = db.relationship('Customer', passive_deletes=True, backref=db.backref('rentals', lazy=True))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id', ondelete='cascade'), nullable=True)
    video = db.relationship('Video', passive_deletes=True, backref=db.backref('rentals', lazy=True))
    due_date = db.Column(db.DateTime, nullable=False, default=week_later)
    checked_out = db.Column(db.Boolean)

# Because the remaining two columns are dynamic, it would be easier to maintain in routes.py
# We could add them as methods in the video model.