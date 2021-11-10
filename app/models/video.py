from app import db
import datetime 

class Video(db.Model):
    __tablename__ = 'videos'
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    customers = db.relationship("Customer", back_populates="videos", secondary="rentals")
    def to_dict(self):
        dictionary = {
            "id": self.video_id,
            "title":self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }
        return dictionary 

    @classmethod
    def validate_id(cls, id):
        try:
            int(id)
        except ValueError:
            return "", 400

        obj = cls.query.get(id)

        if not obj:
            return {
                "message": f"Video {id} was not found"
            }, 404