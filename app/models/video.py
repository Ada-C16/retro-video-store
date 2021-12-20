from app import db

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)

    def to_dict(self):
        video = {
            "id" : self.video_id,
            "title" : self.title,
            "release_date" : self.release_date,
            "total_inventory" : self.total_inventory,
        }

        return video
    
    @classmethod
    def from_dict(cls, request_body):
        video = Video(
            title=request_body["title"],
            release_date=request_body["release_date"],
            total_inventory=request_body["total_inventory"]
        )
        return video
    

