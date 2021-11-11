from app import db
import datetime

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    total_inventory = db.Column(db.Integer)
    # rentals = db.relationship("Customer", secondary="video_rentals", back_populates="videos", lazy=True)

    # Return response body
    def get_video_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "total_inventory": self.total_inventory
        }

    # Video Rental Counter
    def video_rental_count(self):
        counter = 0
        for self.id in self.rentals:
            counter += 1
        return counter


    #Video Inventory Counter 
    def video_inventory(self):
        counter = 0
        for self.id in self.total_inventory:
            counter -= 1
        return counter




