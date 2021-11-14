from app import db
from app.models.rental import Rental

def handle_query_params(cls, request, filter_by={}):

    sort_by = request.args.get("sort")

    if sort_by not in cls.sort_fields:
        return { "error" : "invalid input" }, 400

    if filter_by:
        items = cls.query.filter_by(**filter_by).order_by(sort_by)
    else:            
        items = cls.query.order_by(sort_by)

    return items
