from app import db

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200))
    release_date = db.Column(db.Date)
    total_inventory = db.Column(db.Integer)
    rentals = db.relationship('Rental', backref='video', lazy=True)

    def to_dict(self):
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }
    
    def get_available_inventory(self):
        return self.total_inventory - len(self.rentals)