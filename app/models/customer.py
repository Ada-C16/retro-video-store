from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)
    # videos_checked_out_count = db.Column(db.Integer, default=0, nullable=False)

    def get_videos_checked_out_count(self):
        from app.models.rental import Rental
        videos_checked_out_count = 0

        if Rental.query.filter_by(is_checked_in=True).filter_by(customer_id=self.id) and videos_checked_out_count > 0:
            videos_checked_out_count -= 1    

        return videos_checked_out_count