from flask import Blueprint
from init import db, bcrypt
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

#Quick function that reduces code for adding objects to session
def adder(object):
    db.session.add(object)

#\***************************************************************************\

#Command for seeding tables with example data
@db_commands.cli.command("seed")
def seed_db():

    #Add data for example users, making sure to encrypt passwords
    raphael = Users(
        username = "Raphael", email = "ausraf360@outlook.com", 
        password = bcrypt.generate_password_hash("1234567").decode("utf-8")
    )
    adder(raphael)

    aerolf = Users(
        username = "Aerolf", email = "farsua063@kooltou.com", 
        password = bcrypt.generate_password_hash("7654321").decode("utf-8")
    )
    adder(aerolf)

    #Add data for example cities
    bangkok = Destinations(
        name = "Bangkok", country = "Thailand",
        latitude = 13.736717, longitude = 100.523186
    ) 
    adder(bangkok)

    phuket = Destinations(
        name = "Phuket", country = "Thailand",
        latitude = 8.032003, longitude = 98.333466
    )
    adder(phuket)

    melbourne = Destinations(
        name = "Melbourne", country = "Australia",
        latitude = -37.840935, longitude = 144.946457
    )
    adder(melbourne)

    #Commit users and destinations before making reviews
    db.session.commit()

    #Add data for example reviews for Raphael
    raphael_bangkok = Reviews(
        destination = bangkok.destination_id, user = raphael.user_id,
        date = datetime(2023, 1, 1),
        weather = 4, safety = 3, price = 2, transport = 4, friendliness = 5,
        writing = "Truly the capital of the land of smiles"
    )
    adder(raphael_bangkok)

    raphael_phuket = Reviews(
        destination = phuket.destination_id, user = raphael.user_id,
        date = datetime(2023, 2, 1),
        weather = 5, safety = 3, price = 3, transport = 3, friendliness = 5,
        writing = "Great island paradise"
    )
    adder(raphael_phuket)

    raphael_melbourne = Reviews(
        destination = melbourne.destination_id, user = raphael.user_id,
        date = datetime(2023, 3, 1),
        weather = 2, safety = 4, price = 5, transport = 3, friendliness = 4,
        writing = "Prices won't stop going up"
    )
    adder(raphael_melbourne)

    #Add data for example reviews for Aerolf
    aerolf_bangkok = Reviews(
        destination = bangkok.destination_id, user = aerolf.user_id,
        date = datetime(2023, 1, 1),
        weather = 3, safety = 1, price = 2, transport = 2, friendliness = 4,
        writing = "I'm never getting on a moped in Thailand again"
    )
    adder(aerolf_bangkok)

    aerolf_phuket = Reviews(
        destination = phuket.destination_id, user = aerolf.user_id,
        date = datetime(2023, 2, 1),
        weather = 5, safety = 2, price = 3, transport = 3, friendliness = 4,
        writing = "Riding on a moped here was slighlty less terrible"
    )
    adder(aerolf_phuket)

    aerolf_melbourne = Reviews(
        destination = melbourne.destination_id, user = aerolf.user_id,
        date = datetime(2023, 3, 1),
        weather = 1, safety = 5, price = 4, transport = 5, friendliness = 5,
        writing = "No mopeds, good thing too because it won't stop raining"
    )
    adder(aerolf_melbourne)

    #Commit review instances and make notification that seeding was succesful
    db.session.commit()
    print("Tables seeded")

#\***************************************************************************\