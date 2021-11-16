from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental


VIDEO_TITLE = "A Brand New Video"
VIDEO_INVENTORY = 1
VIDEO_RELEASE_DATE = "01-01-2001"

CUSTOMER_NAME = "A Brand New Customer"
CUSTOMER_POSTAL_CODE = "12345"
CUSTOMER_PHONE = "123-123-1234"

def test_customers_overdue_videos(client, one_checked_out_video):
    response = client.get("/rentals/overdue")

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body[0]["video_id"] == 1
    assert response_body[0]["title"] == VIDEO_TITLE
    assert response_body[0]["customer_id"] == 1
    assert response_body[0]["name"] == CUSTOMER_NAME
    assert response_body[0]["postal_code"] == CUSTOMER_POSTAL_CODE
    # assert response_body[0]["due_date"] == "2021-11-13"