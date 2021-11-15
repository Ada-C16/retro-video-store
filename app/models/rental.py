from app import db

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True,nullable=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), primary_key=True,nullable=True)
    due_date = db.Column(db.DateTime)
    videos_checked_out_count = db.Column(db.Integer)
    available_inventory =  db.Column(db.Integer)
    videos_checked_in = db.Column(db.Boolean, default=False)


 
    # foreign key to connect to the video and customer rental?
    # how do we calculate something dynamically and put it in the table

'''
Notes

# from author to book update the author model (specifically with the particular relationship

update the place we are going to with the foreign key and the relationship

we need to do this x2 for video and customer

'''