from init import db, ma

#\***************************************************************************\

class Reviews(db.Model):
    #Define the reviews table name
    __tablename__= "reviews"
    #Set the primary key 
    review_id = db.Column(db.Integer, primary_key=True)

    #Add the user and destination keys, 
    #which cannot be null as they'll also be foreign keys
    destination = db.Column(db.String())
    user = db.Column(db.String())

    #Add the rest of the keys
    date = db.Column(db.Date())
    weather = db.Column(db.Integer())
    safety = db.Column(db.Integer())
    price = db.Column(db.Integer())
    transport = db.Column(db.Integer())
    friendliness = db.Column(db.Integer())

    writing = db.Column(db.String())

#\***************************************************************************\

class Destinations(db.Model):
    #Define the distinations table name
    __tablename__= "destinations"
    #Set the primary key 
    destination_id = db.Column(db.Integer, primary_key=True)

    #Add the rest of the keys
    name = db.Column(db.String())
    country = db.Column(db.String())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())

#\***************************************************************************\

class Users(db.Model):
    #Define the users table name
    __tablename__= "users"
    #Set the primary key 
    user_id = db.Column(db.Integer, primary_key=True)

    #Add the rest of the keys
    username = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())

#\***************************************************************************\

#Reviews schema
class ReviewSchema(ma.Schema):
    class Meta:
        fields = ("review_id", "destination", "user", "date",
                   "weather", "safety", "price", "transport", 
                   "friendliness", "writing")

#Handle schemas for one either one or multiple cards need to be retrieved
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)