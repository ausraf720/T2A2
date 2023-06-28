from flask import Blueprint, jsonify, request, abort
from init import db
from models import Reviews, review_schema, reviews_schema, ReviewSchema
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

    #Add and commit, then return the review data
    db.session.add(new_review)
    db.session.commit()
    return jsonify(review_schema.dump(new_review))

#\***************************************************************************\

@review_bp.route("/<int:id>/", methods=["DELETE"])
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
        

#\***************************************************************************\