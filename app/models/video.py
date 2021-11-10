from app import db
from sqlalchemy.orm import relationship

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    release_date = db.Column(db.Date)
    total_inventory = db.Column(db.Integer)
    # customers = relationship('Customer', secondary='rental', backref='videos')
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }
