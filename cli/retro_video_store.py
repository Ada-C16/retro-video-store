import requests

url = "http://localhost:5000"

def list_videos():
    response = requests.get(url+"/videos")
    return response.json()

def list_customers():
    response = requests.get(url+"/customers")
    return response.json()

def parse_response(response):
    if response.status_code >= 400:
        return None
    
    return response.json()

def create_video(title, release_date, total_inventory):
    query_params = {
        "title": title,
        "release_date": release_date,
        "total_inventory": total_inventory
    }
    response = requests.post(url+"/videos", json=query_params)
    return parse_response(response)

def checkout_video(customer_id, video_id):
    query_params = {
        "customer_id": customer_id,
        "video_id": video_id
    }
    response = requests.post(url+"/rentals/check-out", json=query_params)
    return parse_response(response)

def checkin_video(customer_id, video_id):
    query_params = {
        "customer_id": customer_id,
        "video_id": video_id
    }
    response = requests.post(url+"/rentals/check-in", json=query_params)
    return parse_response(response)
    