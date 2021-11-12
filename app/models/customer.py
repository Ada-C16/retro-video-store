from app import db
from flask import current_app
from sqlalchemy.orm import backref
from app.models.rental import Rental


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    
    videos_checked_out_count = db.Column(db.Integer)
    # backref is creating 2 new attributes as well as establishing the relationship here
    # backref is creating Customer.videos as well as Video.customers    

    videos = db.relationship("Video", secondary="rental", backref="customers")

    # returns the number of videos that an individual customer has checked out
    def customers_checked_out_videos(self):
        rental_query = Rental.query.filter_by(customer_id=self.id)
        return rental_query.count()

    
