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
    # the videos that the customer has are accessed through the rental table
    # the rental is the child of the customer
    # orphan cascade is normally configured only on the "one" side of a one-to-many relationship, and not on the "many" side of a many-to-one or many-to-many relationship.  To force this relationship to allow a particular "Video" object to be referred towards by only a single "Customer" object at a time via the Customer.videos relationship, which would allow delete-orphan cascade to take place in this direction, set the single_parent=True flag. (Background on this error at: http://sqlalche.me/e/13/bbf0)"
    # videos = db.relationship("Video", secondary="rental", backref="customers")
    videos = db.relationship("Rental", backref='Customer', cascade="all, delete-orphan", lazy="joined")

    # returns the number of videos that an individual customer has checked out
    def customers_checked_out_videos(self):
        rental_query = Rental.query.filter_by(customer_id=self.id, checked_in=False)
        return rental_query.count()

    
