from app import db
from flask import current_app

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)

    rental = db.relationship("Rental",passive_deletes=True, backref="videos")


    def create_video_dict(self):
        return_dict = {
                "id":self.id,
                "title":self.title,
                "release_date":self.release_date,
                "total_inventory": self.total_inventory
                }
        return return_dict