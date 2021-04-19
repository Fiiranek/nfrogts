import time
from db_model import Database
db=Database()

def update_frogs_status(db):
    """ checks if frog reserve date expired """
    # date in seconds

    current_timestamp = round(time.time())
    expire_filter = {'reservation_expire_date': {'$lt': current_timestamp}, 'status': 'reserved'}
    frogs_with_expired_reservation = db.collection.find(expire_filter)
    db.collection.update_many(expire_filter, {
        "$unset": {"reservation_expire_date": ""},
        "$set": {'status': 'free'}
    })


if __name__ == "__main__":
    while True:
        update_frogs_status(db)
        time.sleep(1)
        #print('db sttaus updater working')
