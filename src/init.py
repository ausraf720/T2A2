#SQAlchemy functions as the main ORM
from flask_sqlalchemy import SQLAlchemy

#Marshmallow is used for converting between Python data types, 
# json, and other types
from flask_marshmallow import Marshmallow

#Bcrypt is used for one-way encryption of passwords
from flask_bcrypt import Bcrypt

#JWT used for two-way encryption for tokens,
#  to be provided to logged-in users
from flask_jwt_extended import JWTManager


#Here all of the above modules are stored as variables, 
# so can easily be imported by other files

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()