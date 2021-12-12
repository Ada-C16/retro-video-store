
VIDEO_TITLE = "A Brand New Video"
VIDEO_ID = 1
VIDEO_INVENTORY = 1
VIDEO_RELEASE_DATE = "01-01-2001"

CUSTOMER_NAME = "A Brand New Customer"
CUSTOMER_ID = 1
CUSTOMER_POSTAL_CODE = "12345"
CUSTOMER_PHONE = "123-123-1234"

# -------------Test overdue rental route----------------

def test_no_overdue_videos(client, one_checked_out_video):
    # Act
    response = client.get("/rentals/overdue")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_one_overdue_video(client, one_overdue_video):
    # Act
    response = client.get("/rentals/overdue")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body[0]["video_id"] == VIDEO_ID
    assert response_body[0]["title"] == VIDEO_TITLE
    assert response_body[0]["customer_id"] == CUSTOMER_ID
    assert response_body[0]["name"] == CUSTOMER_NAME
    assert response_body[0]["postal_code"] == CUSTOMER_POSTAL_CODE
    assert response_body[0]["due_date"] == 'Fri, 01 Jun 2018 00:00:00 GMT'
    assert response_body[0]["checkout_date"] == 'Fri, 25 May 2018 00:00:00 GMT'

#---------------Test query params for GET videos---------------

def test_get_videos_sort_by_title(client, three_videos):
    # Act
    query_params = {
        "sort": "title"
    }
    response = client.get("/videos", query_string=query_params)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["title"] == "Babe"
    assert response_body[1]["title"] == "The French Dispatch"
    assert response_body[2]["title"] == "Zoolander"


def test_get_videos_sort_by_release_date(client, three_videos):
    # Act
    query_params = {
        "sort": "release_date"
    }
    response = client.get("/videos", query_string=query_params)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["title"] == "Babe"
    assert response_body[1]["title"] == "Zoolander"
    assert response_body[2]["title"] == "The French Dispatch"

def test_first_page_with_one_result(client, three_videos):
    # Act
    query_params = {
        "p": 1,
        "n": 1
    }
    response = client.get('/videos', query_string=query_params)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["title"] == "Babe"

def test_sort_by_title_only_first_page_two_results(client, three_videos):
    # Act
    query_params = {
        "p": 1,
        "n": 2,
        "sort": "title"
    }
    response = client.get('/videos', query_string=query_params)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["title"] == "Babe"
    assert response_body[1]["title"] == "The French Dispatch"
