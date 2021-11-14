from app import db

class Rental(db.Model):
  __tablename__ = "rentals"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), autoincrement=True, nullable=False)
  video_id = db.Column(db.Integer, db.ForeignKey("video.id"), autoincrement=True, nullable=False)
  due_date = db.Column(db.DateTime)
  customer = db.relationship("Customer", backref="rentals")
  video = db.relationship("Video", backref="rentals")

  def to_dict(self):
    return {
      "id": self.id,
      "customer_id": self.customer_id,
      "video_id": self.video_id,
      "due_date": self.due_date
    }