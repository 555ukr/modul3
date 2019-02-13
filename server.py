import sys
sys.path.insert(0, 'src/')

import json
from flask import Flask, request
from blockchain import Blockchain
from tinydb import TinyDB, Query
from flask import Response

app = Flask(__name__)

@app.route('/transaction', methods=['POST'])
def transaction():
    content = {'please move along': 'nothing to see here'}
    if not Blockchain.submit_tx(request.form['data']):
        return Response(json.dumps({'success':False}), 400, {'ContentType':'application/json'})
    return Response(json.dumps({'success':True}), 200, {'ContentType':'application/json'})

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

@app.route('/getDifficulty', methods=['GET'])
def difficulty():
    db = TinyDB('db/blk.json')
    lst = db.all()[-1:]
    response = app.response_class(
        response=json.dumps(lst[0]['Block Header']['Difficulty Target']),
        status=200,
        mimetype='application/json'
    )
    return response
