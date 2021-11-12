from app import db

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime)
    checked_in = db.Column(db.Boolean, default=False)

    def rental_to_dict(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": len(self.customer.rentals),
            "available_inventory": self.video.total_inventory - len(self.video.rentals),
        }