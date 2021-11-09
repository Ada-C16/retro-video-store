from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    release_date = db.Column(db.String(10))
    total_inventory = db.Column(db.Integer)