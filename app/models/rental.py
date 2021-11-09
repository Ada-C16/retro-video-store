from app import db

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship("Customer", back_populates='rentals')
    
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    video = db.relationship("Video", back_populates='rentals')
    
    due_date = db.Column(db.DateTime)
    
    
    
    def to_json(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": self.?,
            "available_inventory": self.?
          }