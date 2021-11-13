import re
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, jsonify, make_response, request, abort

customer_bp = Blueprint("customers",__name__, url_prefix="/customers")

def valid_int(id,parameter_type):
    try:
        int(id)
    except :
        abort(make_response({"error":f"{parameter_type} must be an integer"},400))
    
def get_customer_from_id(id):
    valid_int(id, "id")
    customer = Customer.query.get(id)
    if customer:
        return customer
    abort(make_response({"message": f"Customer {id} was not found"}, 404))

#CUSTOMER ROUTES
#GET
@customer_bp.route("/<id>", methods=["GET"])
def read_customer(id):
    customer = get_customer_from_id(id)
    response_body = customer.to_dict()

    return jsonify(response_body)


@customer_bp.route("", methods = ["GET"])
def read_all_customers():
    n = request.args.get("n")
    p = request.args.get("p")

    sort_query= request.args.get('sort')

    customers = Customer.query.order_by(Customer.id.asc())

    if sort_query == "name":
        customers = Customer.query.order_by(Customer.name.asc())
    if sort_query == "registered_at":
        customers = Customer.query.order_by(Customer.register_at)
    if sort_query == "postal_code":
        customers = Customer.query.order_by(Customer.postal_code)

    response_body = [customer.to_dict() for customer in customers.paginate(page=p, per_page=n, max_per_page=None).items]
    return jsonify(response_body)
    

#POST 
@customer_bp.route("", methods = ["POST"])
def create_customer():
    form_data = request.get_json()

    if "phone" not in form_data:
        return make_response({"details":"Request body must include phone."},400)

    if "postal_code" not in form_data: 
        return make_response({"details":"Request body must include postal_code."},400)

    if "name" not in form_data:
        return make_response({"details":"Request body must include name."},400)


    new_customer = Customer(
        name = form_data["name"],
        postal_code = form_data["postal_code"],
        phone = form_data["phone"],
    )

    db.session.add(new_customer)
    db.session.commit()
    response_body ={"id":new_customer.id}
    return make_response(jsonify(response_body), 201)
    

#PUT
@customer_bp.route("/<id>", methods = ["PUT"])
def update_customer(id):
    customer = get_customer_from_id(id)
    form_data = request.get_json()

    if  "name" not in form_data or "postal_code" not in form_data or "phone" not in form_data:
            response_body = {"details": "Invalid data"}
            return make_response(jsonify(response_body), 400)

    customer.name = form_data["name"]
    customer.phone = form_data["phone"]
    customer.postal_code = form_data["postal_code"]
    
    db.session.commit()

    return make_response(jsonify(customer.to_dict()), 200)


#DELETE
@customer_bp.route("/<id>", methods = ["DELETE"])
def delete_customer(id):
    customer = get_customer_from_id(id)
    db.session.delete(customer)
    db.session.commit()
    response_body= {"id": customer.id}
    return make_response(jsonify(response_body), 200)

# Custom endpoint for Wave 02

@customer_bp.route("/<id>/rentals", methods=["GET"])
def videos_customer_has_checked_out(id):
    customer = get_customer_from_id(id)

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


# WAVE 03 Custom endpoint
@customer_bp.route("/<id>/history", methods = ["GET"])

def read_all_past_video_for_customer(id):
    customer = get_customer_from_id(id)
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

