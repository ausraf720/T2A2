from flask import Blueprint, jsonify, request, abort
from init import db, bcrypt, jwt
from models import Users, user_schema, users_schema
from datetime import timedelta
from flask_jwt_extended import create_access_token
from error_handling import error_handler

#Set up the blueprint for all authorisation routes
auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

#Call the error handler function, to ensure errors are dealt with,
# and return json responses
error_handler(auth_bp)

#\***************************************************************************\

#Code for registering a new user, and adding them to the database,
# thus they can later add reviews regarding their travel experiences
@auth_bp.route("/register/", methods=["POST"])
def auth_register():

    #First, obtain json input
    user_fields = user_schema.load(request.json)
                                   
    #Then, create new user object from the input
    new_user = Users(
        username = user_fields["username"],
        email = user_fields["email"],

        #Use one-way encrypted password for security
        password = bcrypt.\
            generate_password_hash(user_fields["password"]).decode("utf-8")
    )

    #This section of code checks if the username or email is taken
    #First query Users table,
    #  for any usernames in the db that match the input username
    name = Users.query.filter_by(username=user_fields["username"]).first()

    #Do the exact same thing as the above line of code, but for emails
    email = Users.query.filter_by(email=user_fields["email"]).first()

    #If either username of email show a result, and end up true, return error
    if name or email:
        return abort(400, description="Email and or name already registered")

    #Otherwsie add and commit the data as it is valid
    else:
        db.session.add(new_user)
        db.session.commit()

        #Return data to indicate successful registration
        return jsonify(user_schema.dump(new_user))

#\***************************************************************************\

#Code for logging user in and providing them a token to perform db operations,
# can also give them their ID again if they forgot it
@auth_bp.route("/login/", methods=["POST"])
def auth_login():
    
    #Obtain information from request
    user_fields = user_schema.load(request.json)

    #Query for Users table db entry that matches with inputted username,
    # to obtain the associate encrypted password,
    # (or nothing if the username is wrong and doesn't exist)
    user = Users.query.filter_by(username=user_fields["username"]).first()

    #If username and or password doesn't match, send error
    if not user or not bcrypt.\
        check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Incorrect username or password")
    
    #Otherwise, generate JWT access token for user
    else:

        #Allow token to last only 1 day
        expiry = timedelta(days=1)
        access_token = create_access_token(identity=str(user.user_id), 
                                           expires_delta=expiry)

        #Return the user info and their new access token
        return jsonify({"User":user.username, "ID": user.user_id,
                        "Token": access_token })

#\***************************************************************************\