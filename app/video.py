from flask import current_app
from app import db


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    video_title = db.Column(db.String)
    release_date = db.Column(db.String)
    total_inventory = db.Column(db.Smallint)

    def video_infromation(self):
        return {
            "id": self.video_id,
            "title": self.video_title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
        }
