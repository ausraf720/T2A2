from flask import Flask
from init import db, ma, bcrypt, jwt
from controllers import db_commands
from routes import review_bp
from authorisation import auth_bp

from dotenv import load_dotenv
import os

#\***************************************************************************\
    
#App main function


app = Flask(__name__)

#Load secrets from .env file
load_dotenv()
PASSWORD = os.environ.get('PASSWORD')
USERNAME = os.environ.get('USERNAME')
PORT_NUM = os.environ.get('PORT_NUM')
DATABASE = os.environ.get('DATABASE')

SECRET_JWT_KEY = os.environ.get('SECRET_JWT_KEY')

#Set database URI
uri = f'postgresql+psycopg2:' + \
    f'//{USERNAME}:{PASSWORD}@localhost:{PORT_NUM}/{DATABASE}'
app.config["SQLALCHEMY_DATABASE_URI"] = uri

#Set JWT key
app.config["JWT_SECRET_KEY"] = SECRET_JWT_KEY

db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

#Register commands
app.register_blueprint(db_commands)
app.register_blueprint(review_bp)
app.register_blueprint(auth_bp)

  
#\***************************************************************************\


