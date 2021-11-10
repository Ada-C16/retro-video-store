from app import db
from app.models.rental import Rental

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    title = db.Column(db.String)
    total_inventory = db.Column(db.Integer)
    release_date = db.Column(db.DateTime, nullable=True)

    #build instance method for creating dict here

    def available_inventory(self):
        current_checked_out = []
        videos=Rental.query.get(self.video_id) 
        for video in videos:
            if video.checked_in == False:
                current_checked_out.append(video)

        num_current_checked_out=len(current_checked_out)

        available_inventory = self.total_inventory - num_current_checked_out

        return available_inventory

