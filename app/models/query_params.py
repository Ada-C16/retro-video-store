from app import db
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video

def handle_query_params(cls, request, filter_by={}):

    sort_by = request.args.get("sort")

    if cls == Rental and sort_by == "name":
        items = Rental.query.join(Customer).order_by(Customer.name)
    elif cls == Rental and sort_by == "title":
        items = Rental.query.join(Video).order_by(Video.title)
    elif filter_by:
        items = cls.query.filter_by(**filter_by).order_by(sort_by)
    else:            
        items = cls.query.order_by(sort_by)

    return items

def validate_query_params(cls, request):
    
    sort_by = request.args.get("sort")

    if sort_by not in cls.sort_fields:
        return { "error" : "invalid input" }, 400