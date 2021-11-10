from flask import current_app
from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }

    @classmethod
    def from_json(self, json):
        return Video(
            title=json["title"],
            release_date=json["release_date"],
            total_inventory=json["total_inventory"]
        )