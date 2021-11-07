from app import db
from marshmallow import Schema, fields


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String)
    release_date=db.Column(db.DateTime, auto_now_add=True)
    total_inventory=db.Column(db.Integer)


    def to_dict(self):
        video_dict = {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }
        return video_dict

# class VideoSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Video

class PutVideoInputSchema(Schema):
    """ 

    Parameters:
     - title (str)
     - total_inventory (int)
     - releae_date (date)
    """
    # the 'required' argument ensures the field exists
    title = fields.Str(required=True)
    total_inventory = fields.Int(required=True)
    release_date = fields.DateTime(required=True, auto_now_add=True, format='%m-%d-%Y')
    # id=fields.Int(required=False)
