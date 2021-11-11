from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime) 
    total_inventory = db.Column(db.Integer)
    

    def video_dict(self):
        return {
            "title": self.title,
            "release_date": self.release_date,
            "inventory": self.inventory
        }