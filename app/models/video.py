from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)

    # Return response body
    def get_video_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "total_inventory": self.total_inventory
        }

    # Guard Clause 
    

