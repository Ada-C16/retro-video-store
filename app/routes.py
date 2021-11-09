from flask import Blueprint, jsonify, make_response, request, g, abort
from app.models.video import Video
from app.models.customer import Customer
from app import db

video_bp = Blueprint("video_bp", __name__, url_prefix="/videos")
customer_bp = Blueprint("customer_bp", __name__, url_prefix="/customers")

@customer_bp.before_request
@video_bp.before_request
def get_model_and_label():
    """This is a function that runs before the request is processed.
    It will set g.model and g.label based on the blueprint being accessed,
    both of which are accessible globally to use in other functions.
    """
    bps={
        "video_bp": (Video, "video"),
        "customer_bp": (Customer, "customer")
    }
    g.model, g.label = bps[request.blueprint]
    # return jsonify({"details": new_video.to_dict()}), 201

# @video_bp.errorhandler(400)
# def invalid_data(errorhandler)

@customer_bp.route("", methods=["POST"])
@video_bp.route("", methods=["POST"])
def create_item():
    model = g.model
    req = request.get_json()

    try:
        new_item = model.new_from_dict(req)
    except KeyError:
        abort(400)

    db.session.add(new_item)

    db.session.commit()

    return jsonify(new_item.to_dict()), 201

@customer_bp.route("", methods=["GET"])
@video_bp.route("", methods=["GET"])
def read_items():
    model = g.model
    items = model.query.all()
    items_response = []
    for item in items:
        items_response.append(item.to_dict())
    return jsonify(items_response), 200

@customer_bp.route("/<id>", methods=["GET"])
@video_bp.route("/<id>", methods=["GET"])
def read_item(id):
    model = g.model
    item = model.get_by_id(id)
    return jsonify(item.to_dict()), 200

# @customer_bp.route("/<id>", methods=["DELETE"])
# @video_bp.route("/<id>", methods=["DELETE"])
# def delete_item():
#     model = g.model