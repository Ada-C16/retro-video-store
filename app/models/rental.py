from app import db



class Rental(db.Model):
    __tablename__ = 'rentals'
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True, nullable=False)
    due_date= db.Column(db.DateTime)
    videos_checked_out_count = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)

    @classmethod
    def calculate_available_inventory(cls):
        from models.video import Video 
        # How do I access information from videos table using foreign key?
        # Video.total_inventory
        # Rental.video_id.total_inventory 
    @classmethod
    def get_videos_checked_out_count(cl):
        from models.customer import Customer
        pass
        # Do I need to access customer_id?
        # return videos_checked_out_count += 1
