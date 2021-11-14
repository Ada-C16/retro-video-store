import requests
url = "https://megan-mariah-retro-video-store.herokuapp.com/"

def list_objects(route, query_params):
    """Defines a function that will return get all method for a route"""
    if len(query_params) == 0:
        response = requests.get(url+f"/{route}")
        return response.json()
    else:
        query_url = url+f"/{route}?"

        query_sort = query_params["sort"]
        query_limit = query_params["n"]
        query_page = query_params["p"]

        not_allowed = ["none", "None"]

        if query_sort == "desc":
            query_url = query_url + "sort=desc"
        else:
            query_url = query_url + "sort=asc"

        if query_limit not in not_allowed:
            query_url = query_url + f"&n={query_limit}"

        if query_page not in not_allowed:
            query_url = query_url + f"&p={query_page}"

        response = requests.get(query_url)
        return response.json()

def create_object(body_dictionary, route):
    """Defines a function that will return post method for a route"""
    response = requests.post(url+f"/{route}", json=body_dictionary)
    return response.json()

def view_object(route, id):
    """Defines a function that will return a specificed item in route"""
    response = requests.get(url+f"/{route}/{id}")
    return response.json()

def update_object(body_dictionary, id, route):
    """Defines a function with update method for a specificed item in route"""
    response = requests.put(url+f"/{route}/{id}", json=body_dictionary)
    return response.json()

def delete_object(route, id):
    """Defines a function with delete method for a specificed item in route"""
    response = requests.delete(url+f"/{route}/{id}")
    return response.json()

def retrieve_rentals(route, id):
    """Defines a function which will retrieve items of a join table for route"""
    response = requests.get(url+f"/{route}/{id}/rentals")
    return response.json()

def rental_status(body_dictionary, status):
    """Defines a function which will update rental status for items in body"""
    response = requests.post(url+f"/rentals/{status}", json=body_dictionary)
    return response.json()

