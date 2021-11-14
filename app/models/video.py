from app import db
from app.models.rental import Rental

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    title = db.Column(db.String)
    total_inventory = db.Column(db.Integer)
    release_date = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        '''takes instance of Customer and returns a formatted dictionary
        that includes instance attributes as key, value pairs'''
        video_dict = {
            "id": self.id,
            "title": self.title,
            "total_inventory": self.total_inventory,
            "release_date": self.release_date
            }
        
        return video_dict

