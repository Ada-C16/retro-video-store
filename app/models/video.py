from app import db
from dataclasses import dataclass


class Video(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime())
    due_date = db.Column(db.DateTime())
    total_inventory = db.Column(db.Integer)
    customers = db.relationship("Customer", secondary="Rentals", backref="videos")


    def to_dict(self):
        return {
            "id": self.id,
            "title" : self.title,
            "release_date" : self.release_date,
            "total_inventory" : self.total_inventory
        }       

    @classmethod
    def from_dict(cls, values):
        return cls(**values)