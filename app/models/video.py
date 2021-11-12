from app import db
from flask import request


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    total_inventory = db.Column(db.Integer, nullable=False)
    rentals = db.relationship("Rental", backref="video")

    def create_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }

    def update(self, form_data):
        self.title = form_data["title"]
        self.release_date = form_data["release_date"]
        self.total_inventory = form_data["total_inventory"]

        db.session.commit()

    @classmethod
    def from_json(cls):
        request_body = request.get_json()

        new_video = Video(
            title=request_body["title"],
            release_date=request_body["release_date"],
            total_inventory=request_body["total_inventory"]
        )
        db.session.add(new_video)
        db.session.commit()

        return new_video
