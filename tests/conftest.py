import pytest
from app import create_app
from app.models.video import Video
from app.models.customer import Customer
from app import db
from datetime import datetime
from flask.signals import request_finished

VIDEO_TITLE = "A Brand New Video"
VIDEO_INVENTORY = 1
VIDEO_RELEASE_DATE = "01-01-2001"

CUSTOMER_NAME = "A Brand New Customer"
CUSTOMER_POSTAL_CODE = "12345"
CUSTOMER_PHONE = "123-123-1234"

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_video(app):
    new_video = Video(
        title=VIDEO_TITLE, 
        release_date=VIDEO_RELEASE_DATE,
        total_inventory=VIDEO_INVENTORY,
        )
    db.session.add(new_video)
    db.session.commit()

@pytest.fixture
def one_customer(app):
    new_customer = Customer(
        name=CUSTOMER_NAME,
        postal_code=CUSTOMER_POSTAL_CODE,
        phone=CUSTOMER_PHONE
    )
    db.session.add(new_customer)
    db.session.commit()

@pytest.fixture
def one_checked_out_video(app, client, one_customer, one_video):
    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 1
    })

@pytest.fixture
def three_videos(app):
    db.session.add_all([
        Video(
            title="Brand new video", release_date="02-02-2003", total_inventory=2),
        Video(
            title="Another video", release_date="02-02-2002", total_inventory=3),
        Video(
            title="Final video", release_date="04-06-1990", total_inventory=1)
    ])
    db.session.commit()

@pytest.fixture
def three_customers(app):
    db.session.add_all([
        Customer(
            name="Mary Claire", phone="5555555555", postal_code="44444"),
        Customer(
            name="Trenisha Tea", phone="2223334444", postal_code="11111"),
        Customer(
            name="Candy Corn", phone="1238675309", postal_code="22222")
    ])
    db.session.commit()

