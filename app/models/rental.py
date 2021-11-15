from app import db
from datetime import date, timedelta

class Rental(db.Model):
  __tablename__ = "rentals"
  rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"), autoincrement=True, nullable=False)
  video_id = db.Column(db.Integer, db.ForeignKey("video.video_id"), autoincrement=True, nullable=False)
  due_date = db.Column(db.DateTime, default= date.today() + timedelta(days=7), nullable=False)

  def to_dict(self):
    return {
      "rental_id": self.rental_id,
      "customer_id": self.customer_id,
      "video_id": self.video_id,
      "due_date": self.due_date
    }
