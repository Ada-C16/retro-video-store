from _typeshed import Self
from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.Date) #????
    total_inventory = db.Column(db.Integer)

    def video_dict(self):
        title = self.title
        release_date = self.release_date
        inventory = self.inventory
