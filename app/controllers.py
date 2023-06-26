from flask import Blueprint
from init import db
from models import Reviews, Destinations, Users

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
    raphael = Users(
        username = "Raphael Florea",
        email = "ausraf360@outlook.com",
        password = "12345"
    )
    db.session.add(raphael)

    aerolf = Users(
        username = "Aerolf Leahpar",
        email = "farsua063@kooltou.com",
        password = "54321"
    )
    db.session.add(aerolf)

    bangkok = Destinations(
        name = "Bangkok",
        country = "Thailand",
        latitude = 13.736717,
        longitude = 100.523186
    )
    db.session.add(bangkok)

    phuket = Destinations(
        name = "Phuket",
        country = "Thailand",
        latitude = 8.032003,
        longitude = 98.333466
    )
    db.session.add(phuket)

    melbourne = Destinations(
        name = "Melbourne",
        country = "Australia",
        latitude = -37.840935,
        longitude = 144.946457
    )
    db.session.add(melbourne)

    #Commit instances and make notification
    db.session.commit()
    print("Tables seeded")

#\***************************************************************************\