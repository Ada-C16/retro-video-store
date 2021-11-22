from app import db
from datetime import date
from flask import make_response, abort
from .rental import Rental


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime, default= date.today())
    videos = db.relationship("Video", secondary="rental", backref="customers")

    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "register_at": self.register_at
        }


    @classmethod
    def get_all_records_for_model(cls, query_param):
        if query_param == "name":
            return cls.query.order_by(cls.name.asc())
        elif query_param == "registered_at":
            return cls.query.order_by(cls.register_at)
        elif query_param == "postal_code":
            return cls.query.order_by(cls.postal_code)
        else:
            return cls.query.order_by(cls.id)

    @classmethod
    def from_json(cls, json):

        cls.validate_request(json)

        return cls(
            name=json["name"],
            postal_code=json["postal_code"],
            phone=json["phone"]
        )

    @classmethod
    def validate_request(cls, json):
        if "phone" not in json:
            return abort(make_response({"details":"Request body must include phone."},400))
        if "postal_code" not in json: 
            return abort(make_response({"details":"Request body must include postal_code."},400))
        if "name" not in json:
            return abort(make_response({"details":"Request body must include name."},400))

    @classmethod
    def valid_int(cls, number):
        try:
            int(number)
        except:
            abort(make_response({"error": f"Customer id must be an int"}, 400))
            
        customer = cls.query.get(number)
        if customer:
            return customer

        abort(make_response({"message": f"Customer {number} was not found"}, 404))


    def update_record(self,json):
        self.validate_request(json)
        self.name = json["name"]
        self.phone = json["phone"]
        self.postal_code = json ["postal_code"]
        return self

    @classmethod
    def current_associated_records(cls, id):

        customer = cls.valid_int(id)

        videos_checked_out = []

        for video in customer.videos:
            rental_record = Rental.query.filter_by(customer_id=id, video_id=video.id, return_date=None).first()
            video_info = {
                "release_date": video.release_date,
                "title": video.title,
                "due_date": rental_record.due_date
            }

            videos_checked_out.append(video_info)

        return videos_checked_out