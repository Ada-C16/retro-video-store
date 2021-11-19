from app import db
from .video import Video 
from .customer import Customer


class Rental(db.Model):
    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"))
    due_date = db.Column(db.String)
    customer = db.relationship("Customer", backref="rentals")
    video = db.relationship("Video", backref="rentals")
    checked_out = db.Column(db.Boolean, default=False)


    def to_dict(self):
        # rentals = Rental.query.filter(Rental.video_id == self.video_id) 

        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": len(self.customer.rentals),
            "available_inventory": self.video.total_inventory - len(self.video.rentals),
        }

    def rental_dict(self, id):
        video = Video.query.get(id)

        return {
            "release_date": video.release_date,
            "title": video.title,
            "due_date": self.due_date
        }

    def get_rental_by_video(self, id):
        customer = Customer.query.get(id)

        return {
            "due_date": self.due_date,
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code
        }

