from app import db
import datetime

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    total_inventory = db.Column(db.Integer)
    customers = db.relationship("Customer", secondary="rental", back_populates="videos", lazy=True)
    
    
    # Return response body
    def get_video_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "total_inventory": self.total_inventory
        }


    #Video Counter


    #Available Inventory