from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    release_date = db.Column(db.DateTime, nullable = False)
    total_inventory = db.Column(db.Integer, nullable = False)
    