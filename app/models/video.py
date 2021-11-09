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
    
    # def to_basic_dict(self):
    #     "This is a method that returns a dictionary of only the goal id and any ids of associated tasks"
    #     return {"id": self.id}

    # def update(self,video_dict):
    #     "This is a method that updates the object's title attribute"
    #     self.title = video_dict["title"]
    #     return self
    
    # def add_video(self, req):
    #     "This is a method that adds videos based on their ids to the tasks attribute of the goal"
    #     self.video = [Video.get_by_id(video_id) for video_id in req["video_ids"]]
    #     return self

    @classmethod
    def new_from_dict(cls,video_dict):
        "This method creates a new video object from a dictionary of attributes"

        if "title" not in video_dict:
            abort(make_response({"details": "Request body must include title."}, 400))
        if "release_date" not in video_dict:
            abort(make_response({"details": "Request body must include release_date."}, 400))
        if "total_inventory" not in video_dict:
            abort(make_response({"details": "Request body must include total_inventory."}, 400))


        return cls(
            title=video_dict["title"],
            release_date=video_dict["release_date"],
            total_inventory=video_dict["total_inventory"]
            )   

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
    
    


