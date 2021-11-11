from app import db

class Rental(db.Model):

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True,nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), primary_key=True,nullable=False)
    videos_checked_out_count = db.Column(db.Integer)
    due_date = db.Column(db.DateTime)
