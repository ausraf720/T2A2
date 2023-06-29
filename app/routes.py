from flask import Blueprint, jsonify, request, abort
from sqlalchemy import select, func
from init import db
from models import Reviews, review_schema, reviews_schema, ReviewSchema
from flask_jwt_extended import jwt_required
from datetime import date

review_bp = Blueprint('reviews', __name__, url_prefix="/reviews")

#CRUD OPERATIONS BELOW
#\***************************************************************************\

#Retrieve all reviews route endpoint
@review_bp.route("/", methods=["GET"])
def get_reviews():
    
    reviews_list = Reviews.query.all()
    result = reviews_schema.dump(reviews_list)
    return jsonify(result)

#\***************************************************************************\

#Post new review route endpoint

@review_bp.route("/", methods=["POST"])
@jwt_required()
def post_review():

    #Create new review
    review_fields = ReviewSchema().load(request.json)

    #Fetch data from json request to be put into table
    new_review = Reviews(
        destination = review_fields["destination"], 
        user = review_fields["user"],
        date = date.today(),

        weather = review_fields["weather"], 
        safety = review_fields["safety"], 
        price = review_fields["price"], 
        transport = review_fields["transport"], 
        friendliness = review_fields["friendliness"],

        writing = review_fields["writing"]
    )

    #Add and commit, then return the review data to confirm it works
    db.session.add(new_review)
    db.session.commit()
    return jsonify(review_schema.dump(new_review))

#\***************************************************************************\

@review_bp.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
def delete_review(id):

    bad_review = Reviews.query.filter_by(review_id=id).first()
    
    #Return an error if review doesn't exist
    if not bad_review:
        return abort(400, description= "Review does not exist")
    
    #Otherwise delete review
    else:
        db.session.delete(bad_review)
        db.session.commit()
        return jsonify(review_schema.dump(bad_review))

#\***************************************************************************\

@review_bp.route("/<int:id>/", methods=["PUT", "PATCH"])
@jwt_required()
def update_review(id):

    review_fields = ReviewSchema().load(request.json)
    old_review = Reviews.query.filter_by(review_id=id).first()
    
    #Return an error if review doesn't exist
    if not old_review:
        return abort(400, description= "Review does not exist")
    
    #Otherwise delete review
    else:

        old_review.weather = review_fields["weather"], 
        old_review.safety = review_fields["safety"], 
        old_review.price = review_fields["price"], 
        old_review.transport = review_fields["transport"], 
        old_review.friendliness = review_fields["friendliness"],
        old_review.writing = review_fields["writing"]

        db.session.commit()
        return jsonify(review_schema.dump(old_review))
    

#SPECIAL OPERATIONS
#\***************************************************************************\

#Get all reviews from particular user, anybody can access so no jwt here
@review_bp.route("/for_user/<int:id>/", methods=["GET"])
def get_reviews_for_user(id):

    stmt = select(Reviews).where(Reviews.user==id)
    reviews_list_for_user = db.session.scalars(stmt).all()

    result = reviews_schema.dump(reviews_list_for_user)
    return jsonify(result)

#\***************************************************************************\

#Get average scores for a particular destination, no jwt again

@review_bp.route("/avg/<int:id>", methods=["GET"])
def get_avg_scores(id):

    
    stmt = select(Reviews.price, Reviews.friendliness, 
                  Reviews.safety, Reviews.transport, 
                  Reviews.weather).where(Reviews.destination==id)
    
    reviews_avg_for_destination = db.session.execute(stmt)
    result = reviews_schema.dump(reviews_avg_for_destination)

    #Code to figure out averages for each, first make dict
    avg_dict = {"friendliness": 0,
                "price": 0,
                "safety": 0,
                "transport": 0,
                "weather": 0}

    #Then iterate through each score type to find average for each
    for score_type in avg_dict.keys():

        count = 0
        for scores in result:
            if score_type in scores.keys():
                count += 1
                avg_dict[score_type] += scores[score_type]
        
        #Check for if count 0, if so, don't calculate avg,
        # otherwise will get DivideByZeroError
        if count != 0:
            avg_dict[score_type] /= count



    return jsonify(avg_dict)


#\***************************************************************************\
