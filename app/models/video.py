from flask import current_app
from app import db
from flask import make_response, abort
from .rental import Rental

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }


    @classmethod
    def validate_request(cls, json):
        if "title" not in json:
            return abort(make_response({"details": "Request body must include title."}, 400))
        if "release_date" not in json:
            return abort(make_response({"details": "Request body must include release_date."}, 400))
        if "total_inventory" not in json:
            return abort(make_response({"details": "Request body must include total_inventory."}, 400))

    @classmethod
    def from_json(cls, json):

        cls.validate_request(json)

        return cls(
            title=json["title"],
            release_date=json["release_date"],
            total_inventory=json["total_inventory"]
        )

    @classmethod
    def get_all_records_for_model(cls, query_param):
        if query_param == "title":
            return cls.query.order_by(cls.title)
        elif query_param == "release_date":
            return cls.query.order_by(cls.release_date)
        else:
            return cls.query.order_by(cls.id)

    @classmethod
    def valid_int(cls, number):
        try:
            int(number)
        except:
            abort(make_response({"error": f"Video id must be an int"}, 400))
            
        video = cls.query.get(number)
        if video:
            return video
        abort(make_response({"message": f"Video {number} was not found"}, 404))

    
    def update_record(self, json):
        self.validate_request(json)
        self.title = json["title"]
        self.release_date = json["release_date"]
        self.total_inventory = json["total_inventory"]
        return self

    @classmethod
    def current_associated_records(cls, id):
        video = cls.valid_int(id)

        customer_list = []

        for customer in video.customers:
            rental_record = Rental.query.filter_by(video_id=id, customer_id=customer.id, return_date=None).first()
            customer_info = {
                "due_date": rental_record.due_date,
                "name": customer.name,
                "phone": customer.phone,
                "postal_code": customer.postal_code
            }

            customer_list.append(customer_info)
        return customer_list