from flask import Blueprint, jsonify
from init import db
from models import Reviews, review_schema, reviews_schema


review_bp = Blueprint('reviews', __name__, url_prefix="/reviews")

#\***************************************************************************\

#GET routes endpoint
@review_bp.route("/", methods=["GET"])
def get_reviews():
    
    reviews_list = Reviews.query.all()
    
    result = reviews_schema.dump(reviews_list)
    
    return jsonify(result)