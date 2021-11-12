from app import db
from flask import current_app
from sqlalchemy.orm import backref


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
