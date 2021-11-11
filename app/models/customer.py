from flask import current_app
from app import db
from app.models.rental import Rental

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)
    videos = db.relationship('Video', secondary='rental',backref='customers')
    

    def to_dict(self):
        customer_dict = {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at,
            }
        
        return customer_dict

    #NOT NEEDED sicne we can query multiple parameters

    # def videos_checked_out(self):
    #     checked_out_list = []
    #     videos_checked_out_by_customers=Rental.filter_by()

    #     for video in videos_checked_out_by_customers:
    #         if video.checked_in == False:
    #             checked_out_list.append(video)
        
    #     num_videos_checked_out=len(checked_out_list)

    #     return num_videos_checked_out

