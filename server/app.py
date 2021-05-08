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


# API_KEY = read_api_key_from_file()


def validate_api_key(req):
    if req.headers.get('API_KEY') == API_KEY:
        return True
    return False


@app.route('/reserve', methods=['POST'])
def reserve():
    token_data = request.json
    token_reservation = db.reserve_token(token_data)
    if token_reservation:
        return {'msg': f'Token {token_data["token_id"]} reserved'}
    return {'msg': 'Token NOT reserved'}


@app.route('/getFree')
def getFree():
    free_token_data = db.get_free_token()
    if free_token_data:
        return {
            'amount': free_token_data['amount'],
            'token_id': free_token_data['token_id']
        }
    is_any_token_reserved = db.check_if_any_token_is_reserved()
    if is_any_token_reserved:
        return {
            'msg': 'All tokens reserved'
        }
    return {
        'msg': 'All tokens sold out'
    }


if __name__ == '__main__':
    app.run()
