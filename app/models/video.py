from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.String)
    total_inventory = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }

    #finds the number of videos that are checked out from that video id
    def find_rentals(self, video_id):   
        from .rental import Rental 
        count= 0
        rentals = Rental.query.all()
        for rental in rentals:
            if rental.video_id == video_id:
                count += 1
        return count

    def get_available_inventory(self):
        return self.total_inventory - self.find_rentals(self.id)

    # we need the video id of the rental and get the inventory attribute of that
    # minus find_rentals with video id 