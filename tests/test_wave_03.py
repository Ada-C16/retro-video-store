from app.models.video import Video
from app.models.customer import Customer

# --------------------------------
# ----------- VIDEOS -------------
# --------------------------------

def test_get_videos_sorted_by_title(client, three_videos):
    # Act
    response = client.get("/videos?sort=title")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["title"] == "Another video"
    assert response_body[1]["title"] == "Brand new video"
    assert response_body[2]["title"] == "Final video"

def test_get_videos_sorted_by_release_date(client, three_videos):
    # Act
    response = client.get("/videos?sort=release_date")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["title"] == "Final video"
    assert response_body[1]["title"] == "Another video"
    assert response_body[2]["title"] == "Brand new video"

def test_get_videos_when_sort_query_is_invalid(client, three_videos):
    # Act
    response = client.get("/videos?sort=random_word_that_is_not_sort_query")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3

    assert response_body[0]["title"] == "Brand new video"
    assert response_body[0]["id"] == 1 

    assert response_body[1]["title"] == "Another video"
    assert response_body[1]["id"] == 2 

    assert response_body[2]["title"] == "Final video"
    assert response_body[2]["id"] == 3 

def test_get_certain_number_of_videos(client, three_videos):
    # Act
    response = client.get("/videos?n=2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2

    assert response_body[0]["title"] == "Brand new video"
    assert response_body[0]["id"] == 1 

    assert response_body[1]["title"] == "Another video"
    assert response_body[1]["id"] == 2 

def test_get_certain_number_of_videos_by_page(client, three_videos):
    # Act
    response = client.get("/videos?n=1&p=2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1

    assert response_body[0]["title"] == "Another video"
    assert response_body[0]["id"] == 2 

def test_get_certain_num_of_vids_by_page_sort_by_title(client, three_videos):
    # Act
    response = client.get("/videos?sort=title&n=1&p=2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1

    assert response_body[0]["title"] == "Brand new video"
    assert response_body[0]["id"] == 1

# --------------------------------
# ---------- CUSTOMERS -----------
# --------------------------------

def test_get_customers_sorted_by_name(client, three_customers):
    # Act
    response = client.get("/customers?sort=name")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["name"] == "Candy Corn"
    assert response_body[1]["name"] == "Mary Claire"
    assert response_body[2]["name"] == "Trenisha Tea"

def test_get_customers_sorted_by_phone(client, three_customers):
    # Act
    response = client.get("/customers?sort=phone")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["phone"] == "1238675309"
    assert response_body[1]["phone"] == "2223334444"
    assert response_body[2]["phone"] == "5555555555"

def test_get_customers_sorted_by_postal_code(client, three_customers):
    # Act
    response = client.get("/customers?sort=postal_code")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["postal_code"] == "11111"
    assert response_body[1]["postal_code"] == "22222"
    assert response_body[2]["postal_code"] == "44444"

def test_get_customers_when_sort_query_is_invalid(client, three_customers):
    # Act
    response = client.get("/customers?sort=random_word_that_is_not_sort_query")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3

    assert response_body[0]["name"] == "Mary Claire"
    assert response_body[0]["id"] == 1 

    assert response_body[1]["name"] == "Trenisha Tea"
    assert response_body[1]["id"] == 2 

    assert response_body[2]["name"] == "Candy Corn"
    assert response_body[2]["id"] == 3 

def test_get_certain_number_of_customers(client, three_customers):
    # Act
    response = client.get("/customers?n=2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2

    assert response_body[0]["name"] == "Mary Claire"
    assert response_body[0]["id"] == 1 

    assert response_body[1]["name"] == "Trenisha Tea"
    assert response_body[1]["id"] == 2 

def test_get_certain_number_of_customers_by_page(client, three_customers):
    # Act
    response = client.get("/customers?n=1&p=2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1

    assert response_body[0]["name"] == "Trenisha Tea"
    assert response_body[0]["id"] == 2 

def test_get_certain_num_of_customers_by_page_sort_by_name(client, three_customers):
    # Act
    response = client.get("/customers?sort=name&n=1&p=2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1

    assert response_body[0]["name"] == "Mary Claire"
    assert response_body[0]["id"] == 1