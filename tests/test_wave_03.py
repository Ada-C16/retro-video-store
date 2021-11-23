from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from datetime import datetime, timedelta

VIDEO_TITLE = "A Brand New Video"
VIDEO_ID = 1
VIDEO_INVENTORY = 1
VIDEO_RELEASE_DATE = "01-01-2001"

CUSTOMER_NAME = "A Brand New Customer"
CUSTOMER_ID = 1
CUSTOMER_POSTAL_CODE = "12345"
CUSTOMER_PHONE = "123-123-1234"

DATE_TODAY = datetime.utcnow() + timedelta(days=16)


def test_get_no_videos_overdue(client, one_checked_out_video) :
    # Act
    response = client.get("/rentals/overdue")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_videos_checked_out_history(client, one_checked_in_video):
    # Act
    response = client.get("/videos/1/history")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    len(response_body) == 1
    assert response_body[0]["video"] == VIDEO_TITLE
    assert response_body[0]["video_id"] == VIDEO_ID
    assert response_body[0]["customer_id"] == CUSTOMER_ID
    assert response_body[0]["Customer name"] == CUSTOMER_NAME
    assert response_body[0]["checkout date"] != None
    assert response_body[0]["check-in date"] != None


def test_get_video_checked_out_history_video_not_found(client):
    # Act
    response = client.get("/videos/1/history")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 404
    assert response_body["message"] == "Video 1 was not found"

''' SORTED VIDEOS'''

def test_get_videos_sorted_title_asc(client, four_videos):
    # Act
    response = client.get("/videos?sort=title-asc")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert len(response_body) == 4
    assert response_body[0]['title'] == "A beautiful video"
    assert response_body[1]['title'] == "Blueprint"
    assert response_body[2]['title'] == "Names and names"
    assert response_body[3]['title'] == "Narnia"


def test_get_videos_sorted_release_date_asc(client, four_videos):
    # Act
    response = client.get("/videos?sort=release-date-asc")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert len(response_body) == 4
    assert response_body[0]['title'] == "Blueprint"
    assert response_body[1]['title'] == "Narnia"
    assert response_body[2]['title'] == "Names and names"
    assert response_body[3]['title'] == "A beautiful video"

    
'''CUSTOMERS '''

def test_get_customer_history_customer_not_found(client):
    response = client.get("/customer/1/history")

    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body["message"] == "Customer 1 was not found"

def test_get_customer_history(client, one_checked_in_video):
    # Act
    response = client.get("/customers/1/history")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    len(response_body) == 1
    assert response_body[0]["title"] == VIDEO_TITLE
    assert response_body[0]["checkout_date"] != None
    assert response_body[0]["due_date"] == None

