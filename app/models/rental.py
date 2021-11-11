from app import db
from datetime import timedelta, date

class Rental(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True,nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True,nullable=False)
    due_date = db.Column(db.DateTime, default=date.today() + timedelta(days=7))
    return_date = db.Column(db.DateTime, default=None)


    

