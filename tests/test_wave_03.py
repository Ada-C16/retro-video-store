from app.models.video import Video
from app.models.customer import Customer

VIDEO_TITLE = "A Brand New Video"
VIDEO_ID = 1
VIDEO_INVENTORY = 1
VIDEO_RELEASE_DATE = "01-01-2001"

CUSTOMER_NAME = "A Brand New Customer"
CUSTOMER_ID = 1
CUSTOMER_POSTAL_CODE = "12345"
CUSTOMER_PHONE = "123-123-1234"

def test_customer_history(client, one_checked_out_video):
    response = client.get("/customers/1/history")

    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["title"] == VIDEO_TITLE
    assert response_body[0]["checkout_date"]
    assert response_body[0]["due_date"]

def test_customer_no_rental_history(client, one_customer):
    response = client.get("/customers/1/history")

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_invalid_customer_rental_history(client, one_customer):
    response = client.get("/customers/bye")

    assert response.status_code == 400

def test_customer_history_customer_not_found(client, one_customer):
    response = client.get("/customers/10")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Customer 10 was not found"}