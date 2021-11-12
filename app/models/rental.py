from app import db

# join table 
class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    due_date = db.Column(db.DateTime()) # this will be 7 days from the current date
    videos_checkout_count = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "video_id" : self.video_id,
            "due_date" : self.due_date,
            "videos_checked_out_count" : self.videos_checkout_count,
            "available_inventory" : self.available_inventory
        }       
