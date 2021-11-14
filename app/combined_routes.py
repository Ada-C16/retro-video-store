from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from flask import blueprints, request, Blueprint, jsonify, abort, g
from datetime import date, timedelta


customer_bp = Blueprint("customers",__name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


@customer_bp.before_request
@videos_bp.before_request
def get_model():
    blueprints = {
        "customers": Customer,
        "videos": Video
    }
    g.model = blueprints[request.blueprint]


@customer_bp.route("", methods=["GET"])
@videos_bp.route("", methods=["GET"])
def read_all_records():
    model = g.model
    n = request.args.get("n")
    p = request.args.get("p")
    sort_query= request.args.get('sort')
    records = model.get_all_records_for_model(sort_query)
    response_body = [record.to_dict() for record in records.paginate(page=p, per_page=n, max_per_page=None).items]
    return jsonify(response_body)

@customer_bp.route("", methods=["POST"])
@videos_bp.route("", methods=["POST"])
def create_new_record():
    model = g.model
    request_body = request.get_json()
    new_record = model.from_json(request_body)
    db.session.add(new_record)
    db.session.commit()
    return jsonify(new_record.to_dict()), 201

@customer_bp.route("/<id>", methods=["GET"])
@videos_bp.route("/<id>", methods=["GET"])
def read_one_record(id):
    model = g.model
    record = model.valid_int(id)
    return jsonify(record.to_dict())

@customer_bp.route("/<id>", methods=["PUT"])
@videos_bp.route("/<id>", methods=["PUT"])
def update_one_record(id):
    model = g.model
    record = model.valid_int(id)
    request_body = request.get_json()
    record.update_record(request_body)
    db.session.commit()
    return jsonify(record.to_dict())

@customer_bp.route("/<id>", methods=["DELETE"])
@videos_bp.route("/<id>", methods=["DELETE"])
def delete_one_record(id):
    model = g.model
    record = model.valid_int(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify(record.to_dict())

# Custom endpoint for Wave 02

@customer_bp.route("/<id>/rentals", methods=["GET"])
def videos_customer_has_checked_out(id):
    customer = Customer.valid_int(id)

    videos_checked_out = []

    for video in customer.videos:
        rental_record = Rental.query.filter_by(customer_id=id, video_id=video.id, return_date=None).first()
        video_info = {
            "release_date": video.release_date,
            "title": video.title,
            "due_date": rental_record.due_date
        }

        videos_checked_out.append(video_info)

    return jsonify(videos_checked_out), 200

@videos_bp.route("/<id>/rentals", methods=["GET"])
def all_customers_for_checked_out_video(id):
    video = Video.valid_int(id)

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

    return jsonify(customer_list), 200


# WAVE 03 Custom endpoints
@customer_bp.route("/<id>/history", methods = ["GET"])

def read_all_past_video_for_customer(id):
    customer = Customer.valid_int(id)
    past_rentals = Rental.query.filter(Rental.customer_id==id, Rental.return_date!=None).all()
    video_list = []

    for rental in past_rentals:
        video = Video.query.get(rental.video_id)
        customer_data ={
            "title": video.title,
            "checkout_date": rental.checkout_date,
            "due_date": rental.due_date,
            "return_date": rental.return_date
        }

        video_list.append(customer_data)

    return jsonify(video_list),200

@videos_bp.route("/<id>/history", methods=["GET"])

def read_all_customers_with_checkout_video(id):
    video = Video.valid_int(id)

    past_rentals = Rental.query.filter(Rental.video_id==id, Rental.return_date!=None).all()

    customer_list = []

    for rental in past_rentals:
        customer = Customer.query.get(rental.customer_id)
        
        customer_data = {
            "customer_id" : customer.id,
            "name": customer.name,
            "postal_code": customer.postal_code,
            "checkout_date": rental.checkout_date,
            "due_date": rental.due_date
        }

        customer_list.append(customer_data)

    return jsonify(customer_list),200