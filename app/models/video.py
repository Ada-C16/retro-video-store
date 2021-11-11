from flask import current_app
from app import db
from marshmallow import Schema, fields

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String)
    release_date=db.Column(db.DateTime)
    total_inventory=db.Column(db.Integer)

    renters=db.relationship("Customer", secondary="rental", backref="videos")
    rentals=db.relationship("Rental")

    def to_dict(self):
        video_dict = {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }
        # if self.available_inventory is not None:
        #     video_dict["available_inventory"] = self.available_inventory
        return video_dict

class PutVideoInputSchema(Schema):
    """ 

    Parameters:
     - title (str)
     - total_inventory (int)
     - release_date (date)
    """
    # the 'required' argument ensures the field exists
    title = fields.Str(required=True)
    total_inventory = fields.Int(required=True)
    release_date = fields.DateTime(required=True, auto_now_add=True, format='%m-%d-%Y')
    # id=fields.Int(required=False)
