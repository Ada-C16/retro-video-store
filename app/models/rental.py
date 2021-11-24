
from app import db

class Rental(db.Model):
    __tablename__ = "video_rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    due_date = db.Column(db.DateTime) 
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), nullable=False)
    customer = db.relationship("Customer", backref="rentals")
    video = db.relationship("Video", backref="rentals")

    def to_dict(self, available_inventory): 
        """Returns model info as a dictionary. 
        Adds videos_checked_out_count and available_inventory for requirements
        of route's check in/out function"""
        videos_checked_out_count = len(self.customer.rentals)
        if self.id:
            return {
                "customer_id": self.customer_id,
                "video_id": self.video_id,
                "due_date": self.due_date,
                "videos_checked_out_count": videos_checked_out_count,
                "available_inventory": available_inventory
            }
