from app import db

class Video(db.Model):
    __tablename__ = 'videos'
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.DateTime, nullable = False)
    total_inventory = db.Column(db.Integer, nullable = False)
    rentals = db.relationship('Rental', backref='videos', lazy=True)

    def to_dict(self):
        return {
            'id': self.video_id,
            'title': self.title,
            'release_date': self.release_date,
            'total_inventory': self.total_inventory
        }
    
    def gets_available_inventory(self):
        available_inventory = self.total_inventory - len(self.rentals)
        return available_inventory