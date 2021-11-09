from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.DateTime, nullable = False)
    total_inventory = db.Column(db.Integer, nullable = False)

    # additional attributes
    genres = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.String(10), nullable=False)
    user_rating = db.Column(db.Float(10), nullable=False)
    runtime = db.Column(db.Integer(20), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    platforms = db.Column(db.String(1000), nullable=True)