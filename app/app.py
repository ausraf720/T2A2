from flask import Flask
from init import db, ma, bcrypt, jwt
from commands import db_commands
from routes import review_bp
from authorisation import auth_bp

from dotenv import load_dotenv
import os

#\***************************************************************************\

#App main function that notifies Flask where all functionalities are located
def create_app():

    #Initialise app
    app = Flask(__name__)

    #Load secrets from .env file, 
    # inlcuding URI to connect to database which contains password,
    # and JWT key used for encryption
    load_dotenv()
    URI = os.environ.get('URI')
    SECRET_JWT_KEY = os.environ.get('SECRET_JWT_KEY')

    #Set database URI
    app.config["SQLALCHEMY_DATABASE_URI"] = URI

    #Set JWT key
    app.config["JWT_SECRET_KEY"] = SECRET_JWT_KEY

    #Initialise all the modules 
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    #Register all routes and commands here
    app.register_blueprint(db_commands)
    app.register_blueprint(review_bp)
    app.register_blueprint(auth_bp)

    return app
  
#\***************************************************************************\


