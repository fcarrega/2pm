# External libraries
import os
import sys
import click
from tinydb import Query

# Custom libraries
from . import shared
from . import database

# Initialize database connection
db = database.get('industries')

# Group command
@click.group()
def industry():
    pass

# Add industry
@industry.command()
@click.argument('sector')
@click.argument('industry')
def add(sector, industry):
    print("Adding " + sector + "/" + industry + " in database..." )
    db.insert({'sector': sector, 'industry': industry})
    print("Done !")

@industry.command()
@click.argument('sector')
@click.argument('industry')
def remove(sector, industry):
    print("Removing " + sector + "/" + industry + " from database...")
    Industry = Query()
    db.remove((Industry.sector == sector) & (Industry.industry == industry))
    print("Done !")

@industry.command()
def list():
    print("Available sectors / industries couples :")
    industries = db.all()
    for industry in industries:
        print(industry['sector'] + "/" + industry['industry'])
