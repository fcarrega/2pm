# External libraries
import os
import sys
from tinydb import Query

# Custom libraries
import shared
import database


def add(sector, industry, db):
    print("Adding " + sector + "/" + industry + " in database..." )
    db.insert({'sector': sector, 'industry': industry})
    print("Done !")

def remove(sector, industry, db):
    print("Removing " + sector + "/" + industry + " from database...")
    Industry = Query()
    db.remove((Industry.sector == sector) & (Industry.industry == industry))
    print("Done !")

def list(db):
    print("Available sectors / industries couples :")
    industries = db.all()
    for industry in industries:
        print(industry['sector'] + "/" + industry['industry'])

if __name__ == "__main__":
    db = database.get('industries')
    action = sys.argv[1]
    if action == 'add':
        add(sys.argv[2], sys.argv[3], db)
    elif action == 'remove':
        remove(sys.argv[2], sys.argv[3], db)
    elif action == 'list':
        list(db)
    else:
        print("Action not recognized. Correct actions : add, remove, list")
