from flask import Blueprint
from init import db

db_commands = Blueprint('db', __name__)

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