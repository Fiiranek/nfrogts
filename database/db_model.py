import pymongo
from os import path


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
        query = {'amount': amount, 'status': 'free'}
        found_document = self.collection.find(query)
        query_results = [result for result in found_document]
        if len(query_results) == 0:
            # TODO - send refunds to buyer address
            print('send refunds')
        else:
            # create update query and new (sold) status query
            update_query = {'amount': amount, 'status': 'free'}
            new_status = {'$set': {'status': 'sold'}}
            # update record to sold
            self.collection.update_one(update_query, new_status)
            # TODO - mint token
            # TODO - send token to buyer
            print('mint')


if __name__ == "__main__":
    db = Database()
    #db.match_utxo({'amount': 72111561})
