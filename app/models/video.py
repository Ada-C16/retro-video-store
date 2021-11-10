from app import db

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    total_inventory = db.Column(db.Integer)
    release_date = db.Column(db.DateTime, nullable=True)

    #we do not want an attirbute because it wouldn't allow us to track changes happening\
    #simultaneously and would be harder to update
    # number_rented = db.relationship("Rental", backref="video_id")

    #build instance method for creating dict here

    #instance method for calculating available_inventory here
    #query rentals db for all instances connected to video_id
    #sort by those currently chked_out
    #get length of list
    #total inventory - length of list = available
    #return available