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
    name = db.Column(db.String(), nullable=False)
    country = db.Column(db.String(), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)

    #Link to destinations table

#\***************************************************************************\

class Users(db.Model):
    #Define the users table name
    __tablename__= "users"
    #Set the primary key 
    user_id = db.Column(db.Integer, primary_key=True)

    #Add the rest of the keys
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)

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
    date = db.Column(db.Date(), nullable=False)
    weather = db.Column(db.Integer(), nullable=False)
    safety = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    transport = db.Column(db.Integer(), nullable=False)
    friendliness = db.Column(db.Integer(), nullable=False)
    writing = db.Column(db.String(), nullable=False)

    #Code for adding relationships to be displayed,
    #  when user and destination info needed in a review section
    user_info = db.relationship('Users', backref='reviews')
    destination_info = db.relationship('Destinations', backref='reviews')

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
        fields = ("name", "country", "destination_id")

destination_schema = DestinationSchema()
destinations_schema = DestinationSchema(many=True)

#\***************************************************************************\

#Rating scale should only accept 1 to 5
VALID_RATING = [1,2,3,4,5]

#Reviews schema
class ReviewSchema(ma.Schema):

    user_info = fields.Nested('UserSchema', only=("username",), required=False)
    destination_info = fields.Nested('DestinationSchema', 
                                     only=("name", "country",), required=False)

    #Validate each score such they're between 1 and 5 (inclusive)
    price = safety = transport = weather = friendliness = \
        fields.Integer(required=True, validate=OneOf(VALID_RATING)) 
    
    class Meta:
        fields = ("review_id", "destination", "destination_info", 
                  "date", "user", "user_info",
                  "weather", "safety", "price", "transport", 
                   "friendliness", "writing")
        

#Handle schemas for either one or multiple reviews when necessary
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

#\***************************************************************************\