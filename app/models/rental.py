from app import db

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