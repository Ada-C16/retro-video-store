from app import db

# join table 
class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime()) # due_date will be 7 days from the current date
    video = db.relationship('Video', backref='rentals')
    customer = db.relationship('Customer', backref='rentals')
    
    # videos_checkout_count = db.Column(db.Integer)
    # available_inventory = db.Column(db.Integer) # available_inventory will be a video's total_inventory minus the number of rentals associated with that video 
    # (video.total_inventory -video.customers).
    # video = db.relationship('Video', backref='customers')
    # customer = db.relationship('Customer', back_populates='videos')


    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "video_id" : self.video_id,
            "due_date" : self.due_date,
            "videos_checked_out_count" : self.customer.get_count_checked_out(),
            "available_inventory" : self.available_inventory
        }

    # we can make many dictionaries for diff returns