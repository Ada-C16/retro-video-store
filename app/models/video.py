from app import db
from flask import abort, make_response

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "release_date": self.release_date,
            "title": self.title,
            "total_inventory": self.total_inventory
        }

    @classmethod
    def get_by_id(cls, id):
        try:
            int(id)
        except ValueError:
            abort(400)

        video = cls.query.get(id)
        if not video:
            abort(make_response({"message": f"Video {id} was not found"}, 404))
            
        return video


