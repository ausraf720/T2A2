from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
import os

#\***************************************************************************\

#Load secrets from .env file
load_dotenv()
PASSWORD = os.environ.get('PASSWORD')
USERNAME = os.environ.get('USERNAME')
PORT_NUM = os.environ.get('PORT_NUM')
DATABASE = os.environ.get('DATABASE')

app = Flask(__name__)
#Set database URI
uri = f'postgresql+psycopg2:' + \
    f'//{USERNAME}:{PASSWORD}@localhost:{PORT_NUM}/{DATABASE}'
app.config["SQLALCHEMY_DATABASE_URI"] = uri
    
#\***************************************************************************\

#create the database object

db = SQLAlchemy(app)

class Reviews(db.Model):
    # Define the reviews table name
    __tablename__= "reviews"
    # Set the primary key 
    id = db.Column(db.Integer, primary_key=True)
    # Add the user and destination keys, 
    # which cannot be null as they'll also be foreign keys
    destination = db.Column(db.String())
    user = db.Column(db.String())

    # Add the rest of the keys
    date = db.Column(db.Date())
    weather_rating = db.Column(db.Integer())
    safety_rating = db.Column(db.Integer())
    price_rating = db.Column(db.Integer())
    transport_rating = db.Column(db.Integer())
    friendliness_rating = db.Column(db.Integer())

    written_review = db.Column(db.String())

# create app's cli command named create, then run it in the terminal as "flask create", 
# it will invoke create_db function
@app.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@app.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")
