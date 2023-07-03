from flask import Blueprint, jsonify, request, abort
from sqlalchemy import select
from init import db
from models import Reviews, Users, Destinations, \
                    review_schema, reviews_schema, user_schema, \
                    destination_schema, destinations_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
from error_handling import error_handler


review_bp = Blueprint('reviews', __name__, url_prefix="/reviews")

#Activate error handler function for this file
error_handler(review_bp)

#\***************************************************************************\

#Validation function for the CRUD operations,
# such that users cannot perform these operations on reviews of other users,
# and cannot do anything unless logged in
def user_validator(review):

    #Decrypt JWT token to obtain original user id
    user_id = get_jwt_identity()

    #Find related user info by finding db entry that matches the user_id,
    # in the Users table
    user_jwt = Users.query.get(user_id)

    #Check jwt is valid, and that user is correct
    if (not user_jwt) or (str(user_id) != str(review.user)):
        return abort(401, description="Invalid user")

#CRUD OPERATIONS BELOW
#\***************************************************************************\

#This route retrieves all reviews that exist in the database
@review_bp.route("/", methods=["GET"])
def get_reviews():
    
    #This query gets everything from the Reviews table
    reviews_list = Reviews.query.all()

    #Then, the result is made into a dict then returned as json
    result = reviews_schema.dump(reviews_list)
    return jsonify(result), 200

#\***************************************************************************\

#This route allows a particular user to post a review
@review_bp.route("/", methods=["POST"])
@jwt_required()
def post_review():

    #Data is obtained in json form to be put into table
    review_fields = review_schema.load(request.json)
    
    #Here, the review object is created
    new_review = Reviews(

        #These fields are the main information for the review
        destination = review_fields["destination"], 
        user = review_fields["user"],
        date = date.today(),

        #These are the various scoring categories
        weather = review_fields["weather"], 
        safety = review_fields["safety"], 
        price = review_fields["price"], 
        transport = review_fields["transport"], 
        friendliness = review_fields["friendliness"],

        #This is the more detailed description
        writing = review_fields["writing"]
    )

    #Check user is valid by calling this function
    user_validator(new_review)

    #Add and commit, then return the review data to confirm success
    db.session.add(new_review)
    db.session.commit()
    return jsonify(review_schema.dump(new_review)), 201

#\***************************************************************************\

#This route is used for updating an existing review
@review_bp.route("/<int:id>/", methods=["PUT", "PATCH"])
@jwt_required()
def update_review(id):

    #First, obtain json data to be used for review update
    review_fields = review_schema.load(request.json)

    #Also query Reviews table to find the review,
    # that matches the given id in the URI
    old_review = Reviews.query.filter_by(review_id=id).first()
    
    #Return an error if review doesn't exist
    if not old_review:
        return abort(404, description= "Review does not exist")
    
    #Otherwise proceed to update review
    else:

        #Check user is valid
        user_validator(old_review)

        #Now replace the old values with the new ones 
        old_review.weather = review_fields["weather"], 
        old_review.safety = review_fields["safety"], 
        old_review.price = review_fields["price"], 
        old_review.transport = review_fields["transport"], 
        old_review.friendliness = review_fields["friendliness"],
        old_review.writing = review_fields["writing"]

        #Commit the changes, and return the newly edited review data,
        # to show success
        db.session.commit()
        return jsonify(review_schema.dump(old_review)), 201

#\***************************************************************************\

#This route deals with allowing a user to delete one of their reviews
@review_bp.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
def delete_review(id):

    #First, query the Reviews table to find the review,
    # that matches the given id in the URI
    bad_review = Reviews.query.filter_by(review_id=id).first()
    
    #Return an error if review doesn't exist
    if not bad_review:
        return abort(404, description= "Review does not exist")
    
    #Otherwise delete review
    else:

        #Check user is valid
        user_validator(bad_review)

        #Once validated, delete review and commit
        db.session.delete(bad_review)
        db.session.commit()

        #Finally return bad review to indicate successful deletion
        return jsonify({"review_id": str(id), "user": bad_review.user,
                        "destination": bad_review.destination}), 200 

#SPECIAL OPERATIONS
#\***************************************************************************\

#Get all destinations, so users can check id for each destination
@review_bp.route("/destinations/", methods=["GET"])
def get_dests():
    
    #This query gets everything from the Destinations table
    dests_list = Destinations.query.all()

    #Then, the result is made into a dict then returned as json
    result = destinations_schema.dump(dests_list)
    return jsonify(result), 200

#\***************************************************************************\

#Get all reviews from particular user, anybody can access so no jwt here
@review_bp.route("/for_user/<int:id>/", methods=["GET"])
def get_reviews_for_user(id):
    
    #Query Users to check user actually exists and matches URI id
    user = user_schema.dump(Users.query.filter_by(user_id=id).first())
    if not user:

        #Return error if user doesn't exist
        return abort(404, description= "User not found")
    else:
        #This statement queries the Reviews table,
        # where the user id for a row matches the id in the URI
        reviews_list_for_user = Reviews.query.filter_by(user=id)
        result = reviews_schema.dump(reviews_list_for_user)

        #Return another error if user exists but has no reviews
        if not result:
            return abort(404, description= "No reviews found for user")
        else:
            return jsonify(result), 200

#\***************************************************************************\

#MAIN APP FUNCTIONALITY
#This route shows the average scores for each category for a destination
@review_bp.route("/avg/<int:id>", methods=["GET"])
def get_avg_scores(id):

    #Query Destinations to check user actually exists and matches URI id
    dest_info = Destinations.query.filter_by(destination_id=id).first()
    #Convert into dict
    dest = destination_schema.dump(dest_info)

    #Return error if destination doesn't exist
    if not dest:
        return abort(404, description= "Destination does not exist")
    
    else:
        #Query the Reviews table, 
        # such that it selects all rows such that destination id matches URI id
        reviews_list_for_dest = Reviews.query.filter_by(destination=id)

        #Get the result as python dictionary form
        result = reviews_schema.dump(reviews_list_for_dest)

        #Set up the dictionary which will contain the avg values,
        # note it only contains values for score types so far
        avg_dict = {"friendliness": 0,
                    "price": 0,
                    "safety": 0,
                    "transport": 0,
                    "weather": 0}

        #Then iterate through each score type to find average for each
        for score_type in avg_dict.keys():

            #Average is calculated as  (sum of all scores)/(num of scores)
            count = 0 #Number of scores
            for scores in result:
                if score_type in scores.keys():
                    count += 1
                    avg_dict[score_type] += scores[score_type]
            
            #Check for if count 0, if so, don't calculate avg,
            # otherwise will get DivideByZeroError
            if count != 0:

                #Calculate average for given score type
                avg_dict[score_type] /= count
        

        #Add destination name from dest query at start of function
        avg_dict["place name"] = dest["name"]

        #Return the json object containing the average scores
        return jsonify(avg_dict), 200


#\***************************************************************************\
