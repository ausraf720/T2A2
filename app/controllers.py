from flask import Blueprint
from init import db
from models import Reviews, Destinations, Users
from datetime import datetime

db_commands = Blueprint('db', __name__)

#\***************************************************************************\

#Command for creating all tables
@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

#Command for dropping all tables
@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")

#\***************************************************************************\

#Command for seeding tables with example data
@db_commands.cli.command("seed")
def seed_db():

    #Add data for example users
    raphael = Users(
        username = "Raphael",
        email = "ausraf360@outlook.com", password = "12345"
    )
    db.session.add(raphael)

    aerolf = Users(
        username = "Aerolf", 
        email = "farsua063@kooltou.com", password = "54321"
    )
    db.session.add(aerolf)

    #Add data for example cities
    bangkok = Destinations(
        name = "Bangkok", country = "Thailand",
        latitude = 13.736717, longitude = 100.523186
    ) 
    db.session.add(bangkok)

    phuket = Destinations(
        name = "Phuket", country = "Thailand",
        latitude = 8.032003, longitude = 98.333466
    )
    db.session.add(phuket)

    melbourne = Destinations(
        name = "Melbourne", country = "Australia",
        latitude = -37.840935, longitude = 144.946457
    )
    db.session.add(melbourne)

    #Add data for example reviews for Raphael
    raphael_bangkok = Reviews(
        destination = "Bangkok", user = "Raphael",
        date = datetime(2023, 1, 1),
        weather = 4, safety = 3, price = 2, transport = 4, friendliness = 5,
        writing = "Truly the capital of the land of smiles"
    )
    db.session.add(raphael_bangkok)

    raphael_phuket = Reviews(
        destination = "Phuket", user = "Raphael",
        date = datetime(2023, 2, 1),
        weather = 5, safety = 3, price = 3, transport = 3, friendliness = 5,
        writing = "Great island paradise"
    )
    db.session.add(raphael_phuket)

    raphael_melbourne = Reviews(
        destination = "Melbourne", user = "Raphael",
        date = datetime(2023, 3, 1),
        weather = 2, safety = 4, price = 5, transport = 3, friendliness = 4,
        writing = "Prices won't stop going up"
    )
    db.session.add(raphael_melbourne)

    #Add data for example reviews for Aerolf
    aerolf_bangkok = Reviews(
        destination = "Bangkok", user = "Aerolf",
        date = datetime(2023, 1, 1),
        weather = 3, safety = 1, price = 2, transport = 2, friendliness = 4,
        writing = "I'm never getting on a moped in Thailand again"
    )
    db.session.add(aerolf_bangkok)

    aerolf_phuket = Reviews(
        destination = "Phuket", user = "Aerolf",
        date = datetime(2023, 2, 1),
        weather = 5, safety = 2, price = 3, transport = 3, friendliness = 4,
        writing = "Riding on a moped here was slighlty less terrible"
    )
    db.session.add(aerolf_phuket)

    aerolf_melbourne = Reviews(
        destination = "Melbourne", user = "Aerolf",
        date = datetime(2023, 3, 1),
        weather = 1, safety = 5, price = 4, transport = 5, friendliness = 5,
        writing = "No mopeds, good thing too because it won't stop raining"
    )
    db.session.add(aerolf_melbourne)

    #Commit instances and make notification
    db.session.commit()
    print("Tables seeded")

#\***************************************************************************\