from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.rental import Rental

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@rentals_bp.route("", methods=["POST"])
def check_out():
    pass


@rentals_bp.route("", methods=["POST"])
def check_in():
    pass


@rentals_bp.route("/customers/<customer_id>/rentals", methods=["GET"])
def get_current_rentals(customer_id):
    pass


@rentals_bp.route("/videos/<customer_id>/rentals", methods=["GET"])
def get_current_customers(customer_id):
    pass
