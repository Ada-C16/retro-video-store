# Wave 01

## Models
- Customer
  - Name (string)
  - Zip code (int)
  - Phone number (string)
  - Register_at datetime (when customer was added to the system)

- Methods:
  - To dict
  - From JSON
  - Validate id
  - Validate request body input
  - Return update response (does this need to be a separate method?)
  - Return date added as a correctly formatted string
  
- Video
  - Title
  - Release_date (datetime)
  - Inventory (no. of copies owned by the video store)

## Routes
CRUD routes for both models

Required endpoints:

1. GET `/customers`
   Typical success response: (200)
  {
    "id": 1,
    "name": "Shelley Rocha",
    "registered_at": "Wed, 29 Apr 2015 07:54:14 -0700",
    "postal_code": 24309,
    "phone": "(322) 510-8695"
  }
  for one item, list of these for get all;
  If no customers, empty array and 200 status

2. GET `/customers/<id>`

    Passing a string as an ID returns a 400 response code

    Return one customer: 
    {
    "id": 2,
    "name": "Curran Stout",
    "registered_at": "Wed, 16 Apr 2014 21:40:20 -0700",
    "postal_code": 94267,
    "phone": "(908) 949-6758"
    }
    404 not found if customer doesn't exist.

    Always return 404 not found if the customer does not exist.

    Response body: 
    {"message": "Customer 1 was not found"}

3. POST `/customers`
   
   Required request body parameters:
   - name
   - postal_code
   - phone


    Post / put:
    must contain: 
    { "details" : "Request body must include {field}"} (name/postal_code/phone)

    Response: 201 created;

    {
    "id": 10034
    }

    400 bad request with detailed errors if not required fields.

4. PUT `/customers/<id>`
   Required request body parameters:
   - name
   - postal_code
   - phone

400 Bad request if request body fields are missing
404 not found if customer id is not found
  
Success:
Status: `200`

json
    { 
    "name" : f"Updated ${CUSTOMER_NAME}",
    "phone" : f"Updated ${CUSTOMER_PHONE}",
    "postal_code": f"Updated ${CUSTOMER_POSTAL_CODE}"
    }


1. DELETE `/customers/<id>`

Response: 200 

{
    "id": 2
}



