import sys
sys.path.insert(0, 'src/')

import json
from flask import Flask, request
from blockchain import Blockchain
from tinydb import TinyDB, Query

app = Flask(__name__)

@app.route('/transaction', methods=['POST'])
def transaction():
    Blockchain.submit_tx(request.form['data'])
    return "OK"

@app.route('/transaction/pending', methods=['GET'])
def mempoll():
    db = TinyDB('db/mempoll.json')
    print(json.dumps(db.all()))
    response = app.response_class(
        response=json.dumps(db.all()),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/', methods=['GET', 'POST'])
def hello():
    return 'Hello, World'
