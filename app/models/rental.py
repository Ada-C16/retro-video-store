from app import db

class Rental(db.Model):
  __tablename__ = "rentals"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), autoincrement=True)
  video_id = db.Column(db.Integer, db.ForeignKey("video.id"), autoincrement=True)
  due_date = db.Column(db.String)
  videos_checked_out_count = db.Column(db.Integer)
  available_inventory = db.Column(db.Integer)

  def to_dict(self):
    return {
      "id": self.id,
      "customer_id": self.customer_id,
      "video_id": self.video_id,
      "due_date": self.due_date,
      "videos_checked_out_count": self.videos_checked_out_count,
      "available_inventory": self.available_inventory
    }