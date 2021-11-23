from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String)
    release_date=db.Column(db.DateTime)
    total_inventory=db.Column(db.Integer)
    rentals = db.relationship("Rental", backref="video", lazy=True)

    def to_json(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "release_date" : self.release_date,
            "total_inventory" : self.total_inventory
        }

    def new_video(self, request_data):
        return Video(
                title=request_data["title"],
                release_date=request_data["release_date"],
                total_inventory=request_data["total_inventory"]
            )