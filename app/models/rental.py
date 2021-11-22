from app import db
from flask import jsonify, make_response

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True, nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String)

    
    def to_dict(self, customer, video):
        """Defines a method for returning a dictionary of instance attributes"""
        return{
            "video_id": self.video_id,
            "customer_id": self.customer_id,
            "videos_checked_out_count": customer.number_of_rentals,
            "available_inventory": video.total_inventory
        }
    
    def rental_status(self, rental_status, video, customer):
        """Depending on whether rental is checked in or out, changes appropriate numbers 
        for video.total_inventory and customer.number_of_rentals"""
        if rental_status == "check-out":
            video.total_inventory -= 1
            customer.number_of_rentals += 1
            self.status = "checked-out"
        
        elif rental_status == "check-in":
            self.status = "checked-in"
            customer.number_of_rentals -= 1 
            video.total_inventory += 1
