from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, make_response,request, abort
from dotenv import load_dotenv
import os


load_dotenv()
customer_bp = Blueprint("customer", __name__,url_prefix="/customers")

#Helper function
def valid_int(number):
    try:
        return int(number)     
    except:
        abort(make_response({"error": f"{number} must be an int"}, 400))
#Helper function
def get_customer_from_id(customer_id):
    customer_id = valid_int(customer_id)
    return Customer.get_or_404(customer_id, description="{Customer not found}")

