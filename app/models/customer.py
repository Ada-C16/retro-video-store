from app import db

class Customer(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime())
    videos = db.relationship("Video", secondary="rental", backref="customers")
    # ^ allows us to view videos associated with a specific customer
    # ^ Video is the child, line 11 maps out the relationship between the Video and Customer models, with rental as the secondary model (aka join table or intermediary table).
    
    # The Rental model recognizes the Customer model as "customer" 


    def get_count_checked_out(self):
        pass

