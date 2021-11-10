from app import db


class Rental(db.Model):
    #added table name to make it plural so it makes more sense in our brains as holding\
    #multiple instances of rentals
    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime)
    #added status attribute to show the status as checked in so that history of rentals are kept\
    #and rentals are tracked as checked_in, allows us to filter to see those currently\
    #checked_out
    status = db.Column(db.#we can decide what data type to make this)

    

    # should available inventory and videos_checked_out be attributes or instance methods or hard coded??

    #build instance method for creating dict
    