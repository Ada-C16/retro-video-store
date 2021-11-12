from app import db
from flask import current_app

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.String, nullable=True)
    total_inventory = db.Column(db.Integer)

    # customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    # customer = db.relationship("Customer", back_ref="videos", lazy= True)
    # rentals = db.relationship("Rental", secondary="rentals", backref="videos")

# 
    customers = db.relationship("Customer", secondary="rental", backref="videos")

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }

    @classmethod
    def from_json(cls, request_body):
        return cls(
            title=request_body["title"],
            release_date=request_body["release_date"],
            total_inventory=request_body["total_inventory"]
        )

