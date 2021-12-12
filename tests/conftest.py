import pytest
from app import create_app
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
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
def one_overdue_video(app, one_checked_out_video):
    late_video = Rental.query.get(1)
    late_video.due_date = datetime(2018, 6, 1)
    db.session.commit()

@pytest.fixture
def three_videos(app):
    Babe = Video(
        title="Babe", 
        release_date="December 14 1995",
        total_inventory=1,
        )
    Zoolander = Video(
        title="Zoolander", 
        release_date="September 28, 2001",
        total_inventory=2,
        )
    French_Dispatch = Video(
        title="The French Dispatch",
        release_date="October 22, 2021",
        total_inventory =0
        )
    db.session.add(Babe)
    db.session.add(Zoolander)
    db.session.add(French_Dispatch)
    db.session.commit()

