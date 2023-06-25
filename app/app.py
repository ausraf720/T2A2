from flask import Flask
from init import db
from controllers import db_commands

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

#Set database URI
uri = f'postgresql+psycopg2:' + \
    f'//{USERNAME}:{PASSWORD}@localhost:{PORT_NUM}/{DATABASE}'
app.config["SQLALCHEMY_DATABASE_URI"] = uri

db.init_app(app)

#Register commands
app.register_blueprint(db_commands)

  
#\***************************************************************************\


