from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement= True, nullable=False)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer, nullable=True)
    customers = db.relationship("Customer", secondary="rental", backref="videos")

    def to_dict(self):
        return {"id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory}