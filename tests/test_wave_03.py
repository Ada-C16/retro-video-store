from operator import contains
from app.models.video import Video
from app.models.customer import Customer

VIDEO_TITLE_2 = "Z Brand New Video"
VIDEO_ID_2 = 1
VIDEO_INVENTORY_2 = 2
VIDEO_RELEASE_DATE_2 = "02-02-2002"

VIDEO_TITLE = "A Brand New Video"
VIDEO_ID = 2
VIDEO_INVENTORY = 1
VIDEO_RELEASE_DATE = "01-01-2001"

CUSTOMER_NAME_2 = "Z Brand New Customer"
CUSTOMER_ID_2 = 1
CUSTOMER_POSTAL_CODE_2 = "92345"
CUSTOMER_PHONE_2 = "923-123-1234"

CUSTOMER_NAME = "A Brand New Customer"
CUSTOMER_ID = 2
CUSTOMER_POSTAL_CODE = "12345"
CUSTOMER_PHONE = "123-123-1234"

# --------------------------------
# ----------- VIDEOS -------------
# --------------------------------

# READ

def test_get_videos_sort_by_title(client, second_video, one_video):
    # Act
    response = client.get("/videos?sort=title")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["title"] == VIDEO_TITLE
    assert response_body[0]["id"] == VIDEO_ID
    assert response_body[0]["total_inventory"] == VIDEO_INVENTORY

    assert response_body[1]["title"] == VIDEO_TITLE_2
    assert response_body[1]["id"] == VIDEO_ID_2
    assert response_body[1]["total_inventory"] == VIDEO_INVENTORY_2

def test_get_videos_sort_by_release_date(client, second_video, one_video):
    # Act
    response = client.get("/videos?sort=release_date")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["title"] == VIDEO_TITLE
    assert response_body[0]["id"] == VIDEO_ID
    assert response_body[0]["total_inventory"] == VIDEO_INVENTORY

    assert response_body[1]["title"] == VIDEO_TITLE_2
    assert response_body[1]["id"] == VIDEO_ID_2
    assert response_body[1]["total_inventory"] == VIDEO_INVENTORY_2

def test_get_videos_sort_by_inventory(client, second_video, one_video):
    # Act
    response = client.get("/videos?sort=total_inventory")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["title"] == VIDEO_TITLE
    assert response_body[0]["id"] == VIDEO_ID
    assert response_body[0]["total_inventory"] == VIDEO_INVENTORY

    assert response_body[1]["title"] == VIDEO_TITLE_2
    assert response_body[1]["id"] == VIDEO_ID_2
    assert response_body[1]["total_inventory"] == VIDEO_INVENTORY_2

# --------------------------------
# ----------- CUSTOMERS ----------
# --------------------------------

def test_get_customers_sort_by_name(client, second_customer, one_customer):
    # Act
    response = client.get("/customers?sort=name")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] == CUSTOMER_NAME
    assert response_body[0]["id"] == CUSTOMER_ID
    assert response_body[0]["phone"] == CUSTOMER_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_NAME_2
    assert response_body[1]["id"] == CUSTOMER_ID_2
    assert response_body[1]["phone"] == CUSTOMER_PHONE_2
    assert response_body[1]["postal_code"] == CUSTOMER_POSTAL_CODE_2

def test_get_customers_sort_by_postal_code(client, second_customer, one_customer):
    # Act
    response = client.get("/customers?sort=postal_code")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] == CUSTOMER_NAME
    assert response_body[0]["id"] == CUSTOMER_ID
    assert response_body[0]["phone"] == CUSTOMER_PHONE
    assert response_body[0]["postal_code"] == CUSTOMER_POSTAL_CODE

    assert response_body[1]["name"] == CUSTOMER_NAME_2
    assert response_body[1]["id"] == CUSTOMER_ID_2
    assert response_body[1]["phone"] == CUSTOMER_PHONE_2
    assert response_body[1]["postal_code"] == CUSTOMER_POSTAL_CODE_2

def test_checkout_video(client, one_video, one_customer):

    response = client.post("/rentals/check-out", json={
        "customer_id": 1,
        "video_id": 1
    })

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["video_id"] == 1
    assert response_body["customer_id"] == 1
    assert response_body["videos_checked_out_count"] == 1
    assert response_body["available_inventory"] == 0

# def test_checkout_video_not_found(client, one_video, one_customer):

#     response = client.post("/rentals/check-out", json={
#         "customer_id": 1,
#         "video_id": 2
#     })

#     assert response.status_code == 404

# def test_checkout_customer_video_not_found(client, one_video, one_customer):

#     response = client.post("/rentals/check-out", json={
#         "customer_id": 2,
#         "video_id": 1
#     })

#     assert response.status_code == 404

# def test_checkout_video_no_video_id(client, one_video, one_customer):

#     response = client.post("/rentals/check-out", json={
#         "customer_id": 1,
#     })

#     assert response.status_code == 400

# def test_checkout_video_no_customer_id(client, one_video, one_customer):

#     response = client.post("/rentals/check-out", json={
#         "video_id": 1,
#     })

#     assert response.status_code == 400

# def test_checkout_video_no_inventory(client, one_checked_out_video):
#     response = client.post("/rentals/check-out", json={
#         "customer_id": 1,
#         "video_id": 1
#     })

#     response_body = response.get_json()

#     assert response.status_code == 400
#     assert response_body["message"] == "Could not perform checkout"

# def test_checkin_video(client, one_checked_out_video):
#     response = client.post("/rentals/check-in", json={
#         "customer_id": 1,
#         "video_id": 1
#     })

#     response_body = response.get_json()

#     assert response.status_code == 200
#     assert response_body["video_id"] == 1
#     assert response_body["customer_id"] == 1
#     assert response_body["videos_checked_out_count"] == 0
#     assert response_body["available_inventory"] == 1

# def test_checkin_video_no_customer_id(client, one_checked_out_video):
#     response = client.post("/rentals/check-in", json={
#         "video_id": 1
#     })

#     assert response.status_code == 400

# def test_checkin_video_no_video_id(client, one_checked_out_video):
#     response = client.post("/rentals/check-in", json={
#         "customer_id": 1
#     })

#     assert response.status_code == 400

# def test_checkin_video_not_found(client, one_checked_out_video):
#     response = client.post("/rentals/check-in", json={
#         "customer_id": 2,
#         "video_id": 1
#     })

#     assert response.status_code == 404

# def test_checkin_customer_not_found(client, one_checked_out_video):
#     response = client.post("/rentals/check-in", json={
#         "customer_id": 1,
#         "video_id": 2
#     })

#     assert response.status_code == 404

# def test_checkin_video_not_checked_out(client, one_video, one_customer):

#     response = client.post("/rentals/check-in", json={
#         "customer_id": 1,
#         "video_id": 1
#     })

#     response_body = response.get_json()

#     assert response.status_code == 400
#     assert response_body == {"message": "No outstanding rentals for customer 1 and video 1"}
    

# def test_rentals_by_video(client, one_checked_out_video):
#     response = client.get("/videos/1/rentals")

#     response_body = response.get_json()

#     response.status_code == 200
#     len(response_body) == 1
#     response_body[0]["name"] == CUSTOMER_NAME

# def test_rentals_by_video_not_found(client):
#     response = client.get("/videos/1/rentals")

#     response_body = response.get_json()

#     assert response.status_code == 404
#     assert response_body["message"] == "Video 1 was not found"

# def test_rentals_by_video_no_rentals(client, one_video):
#     response = client.get("/videos/1/rentals")

#     response_body = response.get_json()

#     assert response.status_code == 200
#     assert response_body == []

# def test_rentals_by_customer(client, one_checked_out_video):
#     response = client.get("/customers/1/rentals")

#     response_body = response.get_json()

#     response.status_code == 200
#     len(response_body) == 1
#     response_body[0]["title"] == VIDEO_TITLE

# def test_rentals_by_customer_not_found(client):
#     response = client.get("/customers/1/rentals")

#     response_body = response.get_json()

#     assert response.status_code == 404
#     assert response_body["message"] == "Customer 1 was not found"

# def test_rentals_by_customer_no_rentals(client, one_customer):
#     response = client.get("/customers/1/rentals")

#     response_body = response.get_json()

#     assert response.status_code == 200
#     assert response_body == []

# def test_can_delete_customer_with_rental(client, one_checked_out_video):
#     # Act
#     response = client.delete("/customers/1")

#     #Assert
#     assert response.status_code == 200

# def test_can_delete_video_with_rental(client, one_checked_out_video):
#     # Act
#     response = client.delete("/videos/1")

#     #Assert
#     assert response.status_code == 200






