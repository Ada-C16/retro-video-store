from app import db

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    total_inventory = db.Column(db.Integer)
    release_date = db.Column(db.DateTime, nullable=True)
    number_rented = db.relationship("Rental", backref="video_id")