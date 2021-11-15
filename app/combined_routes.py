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

# WAVE 02 Custom endpoint

@customer_bp.route("/<id>/rentals", methods=["GET"])
@videos_bp.route("/<id>/rentals", methods=["GET"])
def read_all_current_rentals(id):
    model = g.model
    current_records = model.current_associated_records(id)
    return jsonify(current_records), 200

# WAVE 03 Custom endpoints

@customer_bp.route("/<id>/history", methods = ["GET"])
def read_past_video_rentals(id):
    Customer.valid_int(id)
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
    
    return jsonify(video_list)


@videos_bp.route("/<id>/history", methods=["GET"])
def read_all_past_customers(id):
    Video.valid_int(id)
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

    return jsonify(customer_list)