import pymongo
from os import path
from time import time


class Database:

    def __init__(self):
        """ initialize database """
        credentials = self.read_credentials_file()
        USERNAME = credentials['username']
        PASSWORD = credentials['password']
        DB_NAME = credentials['db_name']
        COLLECTION_NAME = credentials['collection_name']
        self.client = pymongo.MongoClient(
            f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.fxynd.mongodb.net/cluster0?retryWrites"
            "=true&w=majority")
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def read_credentials_file(self):
        basepath = path.dirname(__file__)
        db_credentials_filepath = path.abspath(path.join(basepath, "..", "db_credentials.txt"))

        db_credentials_file = open(db_credentials_filepath, "r")
        for line in db_credentials_file:
            line = line.replace("\n", "")
            if "username" in line:
                USERNAME = line.split(" ")[1]
            elif "password" in line:
                PASSWORD = line.split(" ")[1]
            elif "db_name" in line:
                DB_NAME = line.split(" ")[1]
            elif "collection_name" in line:
                COLLECTION_NAME = line.split(" ")[1]
        db_credentials_file.close()
        return {'username': USERNAME, 'password': PASSWORD, 'db_name': DB_NAME, 'collection_name': COLLECTION_NAME}

    def match_utxo(self, utxo_data):
        """ checks if utxo amount matches record in database """
        # TODO - get address of utxo sender
        # utxo_data['amount'] should be in lovelace
        amount = utxo_data['amount'] / 1000000
        query = {'amount': amount}
        found_document = self.collection.find(query)
        query_results = [result for result in found_document]
        if len(query_results) == 0:
            # TODO - send refunds to buyer address
            print('send refunds')
            return

        else:
            result = query_results[0]
            # check if token with this ADA amount is sold, if so send refunds
            if result['status'] == 'sold':
                # TODO - send refunds to buyer address
                print('send refunds')
                return
            # create update query and new (sold) status query
            query = {'amount': amount}
            new_status = {'$set': {'status': 'sold'}}
            # update record to sold
            self.collection.update_one(query, new_status)
            # TODO - mint token
            # TODO - send token to buyer
            # TODO - send rest of ada to our wallet
            print('mint')
            print('send token to buyer')
            print('send rest of ada to our wallet')

    def get_free_frog(self):
        """ gets free frog from database, should be used only from API """
        query = {'status': 'free'}
        query_result = self.collection.find(query).sort('amount', 1).limit(1)
        query_results = [result for result in query_result]

        if len(query_results) > 0:
            result = query_results[0]
            return result
        return False

    def reserve_frog(self, frog_data):
        """ reserves frog in database, should be used only from API """
        amount = frog_data['amount']
        query = {'amount': amount, 'status': 'free'}
        query_result = self.collection.find(query)
        query_results = [result for result in query_result]

        current_timestamp = round(time())
        reservation_expire_date = current_timestamp + (15 * 60)
        # check if frog is free and amount of ADA is correct
        if len(query_results) > 0:
            new_status = {'$set': {'status': 'reserved', 'reservation_expire_date': reservation_expire_date}}
            self.collection.update_one(query, new_status)
            return True
        return False

    def check_if_any_frog_is_reserved(self):
        """ checks if there is any reserved frog """
        query = {'status': 'reserved'}
        query_result = self.collection.find(query)
        query_results = [result for result in query_result]
        if len(query_results) > 0:
            return True
        return False


if __name__ == "__main__":
    db = Database()
    update_frogs_status(db)
    # siema = db.collection.find({})
    # counter = 0
    # for i in siema:
    #     counter+=1
    # print(counter)
    # db.match_utxo({'amount': 72111561})
