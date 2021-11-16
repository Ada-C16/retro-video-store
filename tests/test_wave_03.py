from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental

def test_customers_overdue_videos(client, one_video, one_customer):
    response = client.get("/rentals/overdue")

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body[0]["video_id"] == 1
    assert response_body[0]["title"] == "Blacksmith Of The Banished"
    assert response_body[0]["customer_id"] == 1
    assert response_body[0]["name"] == "Shelley Rocha"
    assert response_body[0]["postal_code"] == "24309"
    assert response_body[0]["due_date"] == "2021-11-13"