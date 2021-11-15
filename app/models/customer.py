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
    # updated video and customer with cascade
    # When the customer is deleted, all associated rentals are also deleted
    # cascade allows us to "delete the ophans" associated with the customer id 
    videos = db.relationship("Rental", backref='Customer', cascade="all, delete-orphan", lazy="joined")

    # returns the number of videos that an individual customer has checked out
    def customers_checked_out_videos(self):
        rental_query = Rental.query.filter_by(customer_id=self.id, checked_in=False)
        return rental_query.count()

    
