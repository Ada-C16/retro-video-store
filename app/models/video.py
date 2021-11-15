from app import db


class Video(db.Model):
    __tablename__='video'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    customers = db.relationship('Customer', secondary='rentals', backref='video')

    def calculate_available_inventory(self):
        from app.models.rental import Rental
        available_inventory = 0

        # In SQL: SELECT COUNT(*) FROM rental WHERE video_id = self.id
        number_of_rentals_with_given_video_id = Rental.query.filter_by(video_id=self.id).count()

        if Rental.query.filter_by(is_checked_in=True):
            available_inventory += 1

        else:

            available_inventory = self.total_inventory - number_of_rentals_with_given_video_id
        
        return available_inventory