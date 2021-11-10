from app import db

class Video(db.Model):
    __tablename__ = 'videos'
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.DateTime, nullable = False)
    total_inventory = db.Column(db.Integer, nullable = False)
    available_inventory = db.Column(db.Integer, nullable = False)
    rentals = db.relationship('Rental', backref='videos', lazy=True)

    # additional attributes
    # genres = db.Column(db.String(100), nullable=False)
    # rating = db.Column(db.String(10), nullable=False)
    # user_rating = db.Column(db.Float(10), nullable=False)
    # runtime = db.Column(db.Integer, nullable=False)
    # description = db.Column(db.String(1000), nullable=False)
    # platforms = db.Column(db.String(1000), nullable=True)

    def to_dict(self):
        return {
            'id': self.video_id,
            'title': self.title,
            'release_date': self.release_date,
            'total_inventory': self.total_inventory,
            'available_inventory': self.available_inventory
        }
    
    # def new_to_dict(self):
    #     return {
    #         'id': self.id,
    #         'title': self.title,
    #         'release_date': self.release_date,
    #         'total_inventory': self.total_inventory,
    #         'genres': self.genres,
    #         'rating': self.rating,
    #         'user_rating': self.user_rating,
    #         'runtime': self.runtime,
    #         'description': self.description,
    #         'platforms': self.platforms
    #     }