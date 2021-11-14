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
@videos_bp.route("/<id>/rentals", methods=["GET"])
def read_all_current_rentals(id):
    model = g.model
    current_records = model.current_associated_records(id)
    return jsonify(current_records), 200

# WAVE 03 Custom endpoint
@customer_bp.route("/<id>/history", methods = ["GET"])
@videos_bp.route("/<id>/history", methods=["GET"])
def read_all_past_rentals(id):
    model = g.model
    past_records = model.past_associated_records(id)
    return jsonify(past_records),200