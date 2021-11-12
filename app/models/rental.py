from app import db
from datetime import datetime

class Rental(db.Model):
    # goal of the model is to store classes effectively in the database, describes what the piece of data looks like
    # describe model specifically so using Python to interact with the SQL database for us so we don't have to do it manually
    # different classes of data to work in the model, doesn't care about specific details of the customer, need to min amount of data to reference to get the data 
    id = db.Column(db.Integer, primary_key = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime)
    checked_out = db.Column(db.Boolean, default=False)
#     >>> import datetime
# >>> datetime.datetime.now() + datetime.timedelta(days=7) - this would be omre on the back end 
# defining what the model looks like, but where the checkout api, create new rental in the database, video rental is associated with, set due date



# APIS - simple interface to interact with your database, create API - pull it, what you want people to use access, what people to do as part of our application
# public facing apis for them to interact with their api, we handle the back end to update the data
# waze - tell spotify where to play the playlist, send to the endpoint at spotify to recieve data where the user wants to play
# function you are exposing to the user
# well defined user interface to work with it
# sign in end point, spotify - to return data to continue
# what are things user would want to do when using your app***********
# HERE THINGS YOU CAN DO WITH MY APP
# waze can build into their application and call into the app
    due_date = db.Column(db.DateTime)
    
    
# >>> datetime.datetime.now() + datetime.timedelta(days=7)
