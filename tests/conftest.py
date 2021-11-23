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
def four_videos(app):

    db.session.add_all([
        Video(title='Narnia', release_date="01-01-2001", total_inventory=1),
        Video(title= "A beautiful video", release_date="01-05-2021", total_inventory=2),
        Video(title= "Names and names", release_date="07-01-2011", total_inventory=3),
        Video(title= "Blueprint", release_date="10-10-1995", total_inventory=3),
    ])
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
def three_customers(app):

    db.session.add_all([
        Customer(name='Betina de Jesus', postal_code=CUSTOMER_POSTAL_CODE, phone=CUSTOMER_PHONE),
        Customer(name= "Amelia Jonson", postal_code=VIDEO_RELEASE_DATE, phone=CUSTOMER_PHONE),
        Customer(name= "Monica Seller", postal_code=VIDEO_RELEASE_DATE, phone=CUSTOMER_PHONE),
    ])
    db.session.commit()


@pytest.fixture
def one_checked_out_video(app, client, one_customer, one_video):
    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 1
    })

@pytest.fixture
def one_checked_in_video(app, client, one_checked_out_video):
    response = client.post("/rentals/check-in", json={
        "customer_id": 1,
        "video_id": 1
    })






