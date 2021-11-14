from flask import make_response, jsonify
def valid_id_or_400(id):
    """[This function validates the id that a request uses to look up an object in the database. Returns a 400 response if the id is not numeric.]

    Args:
        id ([unicode string]): [The id a request uses to look up an object in the database.]

    Returns:
        [Response instance]: [A 400 response if the id is not numeric. Otherwise None.]
    """
    if not id.isnumeric():
            response_body = {
                'details': 'Invalid video id'
            }
            return make_response(jsonify(response_body), 400)