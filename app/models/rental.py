from app import db
import datetime


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow() + datetime.timedelta(days=7))
    checked_out = db.Column(db.Boolean)
    video = db.relationship("Video", backref="rentals")
    customer = db.relationship("Customer", backref="rentals")


    #pure join table = no other attributes present besides foreign key(s)

    #instead of deleting, mark an attribute on an instance as "deleted" instead of deleting the whole row. 
    #From a data/business perspective; this ensures that records don't disappear.


    #Rental Response Body for Rental Check-outs
    def rental_receipt(self):
        pass
        return {
                "customer_id": self.customer_id,
                "video_id": self.video_id,
                "due_date": self.due_date,
                "videos_checked_out_count": 2,
                "available_inventory": 5
                }

    #Rental Response Body for Rental Check-ins
    