from app import db

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False) #not sure if nullable has to be false
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), nullable=False) #not sure if nullable has to be false
    due_date = db.Column(db.DateTime)

    @classmethod
    def is_data_valid(cls, dict):
        types = {
            "customer_id": int,
            "video_id": int
        }
        for input_type in types:
            if not dict.get(input_type):
                return False
            if type(dict.get(input_type)) != types[input_type]:
                return False
        return True