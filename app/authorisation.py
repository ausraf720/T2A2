from flask import Blueprint, jsonify, request, abort
from init import db, bcrypt
from models import Users, user_schema, users_schema

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

#\***************************************************************************\

#Code for registering a new user
@auth_bp.route("/register/", methods=["POST"])
def auth_register():

    user_fields = user_schema.load(request.json)
    new_user = Users(
    
        username = user_fields["username"],
        email = user_fields["email"],
        #Use encrypted password for security
        password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
    )

    #Add and commit, then return the user data to confirm it works
    db.session.add(new_user)
    db.session.commit()
    return jsonify(user_schema.dump(new_user))

#\***************************************************************************\

@auth_bp.route("/login/", methods=["POST"])
def auth_login():
    
    #Obtain information from request
    user_fields = user_schema.load(request.json)
    user = Users.query.filter_by(username=user_fields["username"]).first()

    #If username and or password doesn't match, send error
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Incorrect username or password")
    
    #Otherwise, return...
    else:
        return "token"

#\***************************************************************************\








#MAY GET DELETED LATER
#\***************************************************************************\

#Retrieve all reviews route endpoint
@auth_bp.route("/", methods=["GET"])
def get_users():
    
    reviews_list = Users.query.all()
    result = users_schema.dump(reviews_list)
    return jsonify(result)

#\***************************************************************************\