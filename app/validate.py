from flask import abort, make_response
from app.models.video import Video
from app.models.customer import Customer


class Validate:
    def valid_id(id):

        try:
            id = int(id)
        except ValueError:
            abort(400)
        return id

    def valid_video(video_id, action=None):
        """If the responses required by the tests werent nearly, but not quite, identical,
        the inner if wouldnt be necessary"""
        video = Video.query.get(video_id)

        if not video:
            if action:
                abort(
                    make_response(
                        {"details": f"Video with id number {video_id} was not found"},
                        404,
                    )
                )

            abort(make_response({"message": f"Video {video_id} was not found"}, 404))
        return video

    def valid_customer(customer_id, action=None):

        customer = Customer.query.get(customer_id)

        if not customer:
            if action:
                abort(
                    make_response(
                        {
                            "details": f"Customer with id number {customer_id} was not found"
                        },
                        404,
                    )
                )
            abort(
                make_response({"message": f"Customer {customer_id} was not found"}, 404)
            )
        return customer

    def missing_fields(request_body, model):

        for field in model.required_fields:
            if field not in request_body:
                return {"details": f"Request body must include {field}."}
        return False
