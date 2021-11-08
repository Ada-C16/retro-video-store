from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement= True, nullable=False)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=True)
    copies = db.Column(db.Integer, nullable=True)

