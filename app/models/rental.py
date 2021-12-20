from app import db

class Rental(db.Model):
    # rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), primary_key=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True, nullable=False)


    due_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime, nullable=True)