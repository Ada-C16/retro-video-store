from app import db

def handle_query_params(cls, request):

        sort_by = request.args.get("sort")

        if sort_by not in cls.sort_fields:
            return { "error" : "invalid input" }, 400

        items = cls.query.order_by(sort_by)

        return items
