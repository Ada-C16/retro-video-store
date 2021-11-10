from app import db
from datetime import datetime, timedelta

class Rental(db.Model):
    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True, nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.video_id'), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime)
    checked_out = db.Column(db.Boolean)

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "checked_out": self.checked_out,
            "due_date": self.due_date.strftime("%Y-%m-%d") if self.due_date else None
        }

    @classmethod
    def from_json(cls, customer_id, video_id):

        now = datetime.now()

        new_rental = cls(
            customer_id = customer_id,
            video_id = video_id,
            checked_out = True,
            due_date = now.timedelta(days=7)
        )
