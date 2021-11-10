# Investigate later
https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.TIMESTAMP

# Wave 02
 
## Models
`Rental` model
`customer_id` Foreign key (int)
`video_id` foreign key (int)
`due_date` 7 days from the current date (guessing DateTime)
`status` checked in / checked out

## Routes
1. `POST /rentals/check-out` - Sarah
   - Sets the due date of the rental to 7 days from the current date
   - Required body parameters:
     - `customer_id` | integer | ID of the customer attempting to check out this video
     - `video_id` | integer | ID of the video to be checked out

   Success reponse: (200)
     {
       "customer_id": 122581016,
       "video_id": 235040983,
       "due_date": "2020-06-31",
       "videos_checked_out_count": 2,
       "available_inventory": 5
     }

   If customer not found: 404
   If video not found: 404
   If missing parameters: 400
   If video does not have any inventory: 400, { "message" : "Could not perform checkout"}

2. `POST /rentals/check-in` - Lilly
   - either delete the rental or change it's status to `"checked_in"`.
   - required body parameters 
    `customer_id` | integer | ID of the customer attempting to check out this video
    `video_id` | integer | ID of the video to be checked out

  - Response: 200
    {
    "customer_id": 122581016,
    "video_id": 277419103,
    "videos_checked_out_count": 1,
    "available_inventory": 6
    }

3. `GET /customers/<customer_id>/rentals` - Sarah
   List the videos a customer currently has checked out.

   Typical success response is a list of videos with the due date:

  Success: status: `200` 

  [
      {
          "release_date": "Wed, 01 Jan 1958 00:00:00 GMT",
          "title": "Vertigo",
          "due_date": "Thu, 13 May 2021 19:27:47 GMT",
      },
      {
          "release_date": "Wed, 01 Jan 1941 00:00:00 GMT",
          "title": "Citizen Kane",
          "due_date": "Thu, 13 May 2021 19:28:00 GMT",
      }
  ]

4. `GET /videos/<id>/rentals` - Lilly

  List the customers who _currently_ have the video checked out

  Success: 200
  [
      {
          "due_date": "Thu, 13 May 2021 21:36:38 GMT",
          "name": "Edith Wong",
          "phone": "(555) 555-5555",
          "postal_code": "99999",
      },
      {
          "due_date": "Thu, 13 May 2021 21:36:47 GMT",
          "name": "Ricarda Mowery",
          "phone": "(555) 555-5555",
          "postal_code": "99999",
      }
  ]



# Wave 01

## Models
- Customer
  - Name (string)
  - Zip code (int)
  - Phone number (string)
  - Register_at datetime (when customer was added to the system)
  - 

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


5. DELETE `/customers/<id>`

Response: 200 

{
    "id": 2
}



