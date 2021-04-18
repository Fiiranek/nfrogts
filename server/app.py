from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from database.db_model import Database
from os import path

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = Database()


def read_api_key_from_file():
    basepath = path.dirname(__file__)
    api_key_filepath = path.abspath(path.join(basepath, "..", "api_key.txt"))

    api_key_file = open(api_key_filepath, "r")
    for line in api_key_file:
        FILE_API_KEY = line.replace("\n", "").split(" ")[1]
    api_key_file.close()
    return FILE_API_KEY


API_KEY = read_api_key_from_file()


def validate_api_key(req):
    if req.headers.get('API_KEY') == API_KEY:
        return True
    return False


@app.route('/reserveFrog', methods=['POST'])
def reserveFrog():
    is_api_key_valid = validate_api_key(request)
    if is_api_key_valid:
        frog_data = request.json
        frog_reservation = db.reserve_frog(frog_data)
        if frog_reservation:
            return {'msg': f'Frog {frog_data["frog_id"]} reserved'}
        return {'msg': 'Frog NOT reserved'}
    return {
        'msg': 'Invalid api key'
    }


@app.route('/getFreeFrog')
def getFreeFrog():
    is_api_key_valid = validate_api_key(request)
    if is_api_key_valid:
        free_frog_data = db.get_free_frog()
        if free_frog_data:
            return {
                'amount': free_frog_data['amount'],
                'frog_id': free_frog_data['frog_id']
            }
        is_any_frog_reserved = db.check_if_any_frog_is_reserved()
        if is_any_frog_reserved:
            return {
                'msg': 'All frogs reserved'
            }
        return {
            'msg': 'All frogs sold out'
        }
    return {
        'msg': 'Invalid api key'
    }


if __name__ == '__main__':
    app.run()
