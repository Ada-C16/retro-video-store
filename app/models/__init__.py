from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    if not test_config:
        app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    else: 
        app.config["TESTING"] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')

    from app.models.customer import Customer
    from app.models.video import Video
    from app.models.rental import Rental

    from .routes import customers_bp, videos_bp, rentals_bp
    app.register_blueprint(customers_bp)
    app.register_blueprint(videos_bp)
    app.register_blueprint(rentals_bp)

    return app