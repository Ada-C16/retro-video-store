from app import db




class Rental(db.Model):
    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'))
    due_date = db.Column(db.DateTime)
    checked_in = db.Column(db.Boolean, default=False)


    #build instance method for creating dict
    