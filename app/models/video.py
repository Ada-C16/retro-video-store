from app import db

class Video(db.Model):
# building the database table with columns, data type, column names
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime) #should this be nullable?
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer, nullable = True)
    

