from database.db_model import Database
from time import time


def update_frogs_status(db: Database):
    """ checks if frog reserve date expired """
    current_date = round(time() * 1000)
    filter = {"$and": [{'reservationExpireDate': {'$lt': current_date}}, {'reservationExpireDate': {
        '$gt': 0}}]}
    db.collection.find(filter)
