from app import db
from flask import abort, make_response


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.Date)
    total_inventory = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
        }

    def update(self, request_body):
        for key, value in request_body.items():
            if key in Video.__table__.columns.keys():
                setattr(self, key, value)

    def check_inventory(self):
        available_inventory = self.total_inventory - len(self.rentals)
        if available_inventory <= 0:
            abort(make_response({"message": "Could not perform checkout"}, 400))
