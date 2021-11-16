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

    def available_inventory(self):
        from app.models.rental import Rental
        out_count = Rental.query.filter_by(video_id = self.id).count()
        available_inventory = self.total_inventory - out_count
        return available_inventory
        