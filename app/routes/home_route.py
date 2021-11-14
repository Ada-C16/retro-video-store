from flask import Blueprint, make_response

home_bp = Blueprint('home', __name__, url_prefix='/')

@home_bp.route('', methods=['GET'])
def go_home():
    return make_response('Popcorn next door --->', 200)