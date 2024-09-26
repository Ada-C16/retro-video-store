import pytest
from app import create_app
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental

from app import db
from datetime import datetime
from flask.signals import request_finished

from tests.test_wave_03 import CUSTOMER_ID, CUSTOMER_ID_2, VIDEO_ID, VIDEO_ID_2

VIDEO_TITLE = "A Brand New Video"
VIDEO_INVENTORY = 1
VIDEO_RELEASE_DATE = "01-01-2001"

VIDEO_TITLE_2 = "Z Brand New Video"
VIDEO_INVENTORY_2 = 2
VIDEO_RELEASE_DATE_2 = "02-02-2002"

CUSTOMER_NAME = "A Brand New Customer"
CUSTOMER_POSTAL_CODE = "12345"
CUSTOMER_PHONE = "123-123-1234"

CUSTOMER_NAME_2 = "Z Brand New Customer"
CUSTOMER_POSTAL_CODE_2 = "92345"
CUSTOMER_PHONE_2 = "923-123-1234"

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
def second_video(app):
    new_video = Video(
        title=VIDEO_TITLE_2, 
        release_date=VIDEO_RELEASE_DATE_2,
        total_inventory=VIDEO_INVENTORY_2,
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
def second_customer(app):
    new_customer = Customer(
        name=CUSTOMER_NAME_2,
        postal_code=CUSTOMER_POSTAL_CODE_2,
        phone=CUSTOMER_PHONE_2
    )
    db.session.add(new_customer)
    db.session.commit()

@pytest.fixture
def one_checked_out_video(app, client, one_customer, one_video):
    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 1,
        "due_date": "11-11-2021"
    })


@pytest.fixture
def two_rentals(app, one_customer, one_video, second_customer, second_video):
    new_rental1 = Rental(
        customer_id=CUSTOMER_ID_2,
        video_id=VIDEO_ID_2,
        due_date="12-12-2021"
    )

    new_rental2 = Rental(
        customer_id=CUSTOMER_ID,
        video_id=VIDEO_ID,
        due_date="11-11-2021"
    )

    db.session.add(new_rental1)
    db.session.add(new_rental2)
    db.session.commit()



