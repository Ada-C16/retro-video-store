from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)


def to_dict(self):
    # if not self.completed_at:
    #     self.completed_at = None
    # if not self.completed_at:
        # task_dict = {
        #     "id": self.task_id,
        #     "title": self.title,
        #     "description": self.description,
        #     "is_complete": False
        # }
        # if self.goal_id:
        #     task_dict["goal_id"] = self.goal_id
        # return task_dict

    # elif self.completed_at:
    return {
        "id": self.id,
        "title": self.title,
        "release_date": self.release_date,
        "total_inventory": self.inventory
    }
