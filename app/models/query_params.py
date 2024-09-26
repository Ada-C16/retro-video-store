from app import db
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video

def handle_query_params(cls, request, filter_by={}):

    sort_by = request.args.get("sort") if request.args.get("sort") else None

    per_page = int(request.args.get("n")) if request.args.get("n") else None

    page = int(request.args.get("p")) if request.args.get("p") else None

    cls_join = None

    if cls == Rental and sort_by == "title":
        cls_join = Video
        sort_by = Video.title
    elif cls == Rental and sort_by == "name":
        cls_join = Customer
        sort_by = Customer.name

    if cls_join:
        items = cls.query.filter_by(**filter_by).join(cls_join).order_by(sort_by).paginate(per_page=per_page, page=page).items
    else:            
        items = cls.query.filter_by(**filter_by).order_by(sort_by).paginate(per_page=per_page, page=page).items
    print(items)
    return items

def validate_query_params(cls, request):
    
    sort_by = request.args.get("sort")

    if sort_by not in cls.sort_fields:
        return { "error" : "invalid input" }, 400