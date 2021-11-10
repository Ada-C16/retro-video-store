from app import db
from sqlalchemy.sql.functions import func

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    # server_default tells sqlA to pass the default value as part of the CREATE TABLE
    # func.now() or func.current_timestamp() - they are aliases of each other. This tells DB to calcaate the timestamp itself
    registered_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def customer_dict(self):
        dict = {
            "id": self.customer_id,
            "name": self.name,
            "phone": self.phone,
            "postal_code": str(self.postal_code),
            # weekday|day of month (16)|month name|year|local version of time|, UTC offset +HHMM or -HHMM
            "registered_at": self.registered_at.strftime("%a, %-d %b %Y %X %z")
    }
    #     if self.registered_at is not None:
    #         dict["registered_at"] = self.registered_at.strfttime("%a, %-d %b %Y %X %z")
            
        return dict