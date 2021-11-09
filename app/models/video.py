from app import db
import datetime 

class Video(db.Model):
    __tablename__ = 'videos'
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    def to_dict(self):
        dictionary = {
            "id": self.video_id,
            "title":self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }
        return dictionary 
