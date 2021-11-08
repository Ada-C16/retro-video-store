from app import db
from flask import request
from app.models.rental import Rental


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    total_inventory = db.Column(db.Integer, nullable=False)
    customer = db.relationship("Customer", secondary=Rental, backref="videos")

    @classmethod
    def from_json(cls):
        request_body = request.get_json()

        new_video = Video(title=request_body["title"],
                          release_date=request_body["release_date"],
                          total_inventory=request_body["total_inventory"]
                          )
        db.session.add(new_video)
        db.session.commit()

        return new_video
