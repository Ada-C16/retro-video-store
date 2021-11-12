from app import db
from app.models.rental import Rental

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    
    def videos_checked_out_count(self):
        """
        We are creating this method here because this is where 
        we have the information about the inventory and with the back ref
        we have access to the rental information.
        """ 
        rental_query = Rental.query.filter_by(video_id=self.id) 
        return rental_query.count() # Here we created a query that we were able to take a count of.

# Don't forget that we only want to count active rentals. 
# Right now, in Wave 2, they haven't required us to provide information about that.

    def available_inventory(self):
        available_inv = self.total_inventory - self.videos_checked_out_count()
        return available_inv