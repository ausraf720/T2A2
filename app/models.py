from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, OneOf

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

    #Link to destinations table

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

class Reviews(db.Model):
    #Define the reviews table name
    __tablename__= "reviews"
    #Set the primary key 
    review_id = db.Column(db.Integer, primary_key=True)

    #Add the user and destination keys, 
    # which cannot be null as they'll also be foreign keys
    destination = db.Column(db.Integer, 
                            db.ForeignKey("destinations.destination_id"), 
                            nullable=False)
    user = db.Column(db.Integer, 
                     db.ForeignKey("users.user_id"), 
                     nullable=False)

    #Add the rest of the keys
    date = db.Column(db.Date())
    weather = db.Column(db.Integer())
    safety = db.Column(db.Integer())
    price = db.Column(db.Integer())
    transport = db.Column(db.Integer())
    friendliness = db.Column(db.Integer())
    writing = db.Column(db.String())

    #Code for adding relationships to be displayed,
    #  when user and destination info needed in a review section
    user_rel = db.relationship('Users', backref='reviews')
    dest_rel = db.relationship('Destinations', backref='reviews')

#\***************************************************************************\

class UserSchema(ma.Schema):

    #Firstly validate inputs so that they exist and password long enough
    password = fields.String(required=True, 
                             validate=Length(min=6, 
                                             error='Password too short'))
    username = fields.String(required=True, 
                             validate=Length(min=1, 
                                             error='Name cannot be empty'))
    email = fields.String(required=False, 
                          validate=Length(min=1, 
                                          error='Email cannot be empty'))

    class Meta:
        fields = ("user_id", "username", "email", "password")

#Handle schemas for either one user when necessary
user_schema = UserSchema()
users_schema = UserSchema(many=True)

#Quick destination schema
class DestinationSchema(ma.Schema):
    class Meta:
        fields = ("name", "country")

#\***************************************************************************\

#Rating scale should only accept 1 to 5
VALID_RATING = [1,2,3,4,5]

#Reviews schema
class ReviewSchema(ma.Schema):

    user_rel = fields.Nested('UserSchema', only=("username",))
    dest_rel = fields.Nested('DestinationSchema')

    #Validate each score such they're between 1 and 5 (inclusive)
    price = safety = transport = weather = friendliness = \
        fields.Integer(required=True, validate=OneOf(VALID_RATING)) 
    
    class Meta:
        fields = ("review_id", "destination", "date", "user",
                  "weather", "safety", "price", "transport", 
                   "friendliness", "writing")
        

#Handle schemas for either one or multiple reviews when necessary
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

#\***************************************************************************\