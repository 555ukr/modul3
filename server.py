import sys
sys.path.insert(0, 'src/')

import json
from flask import Flask, request
from blockchain import Blockchain
from tinydb import TinyDB, Query
from flask import Response
from hashlib import sha256
import binascii

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


@app.route('/getBlockByHeight', methods=['POST'])
def blockReturn():
    heigh = int(request.form['data'])
    db = TinyDB('db/blk.json')
    lst = db.all()[heigh]
    print(lst)
    response = app.response_class(
        response=json.dumps(lst),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/getBlockByHash', methods=['POST'])
def blockReturnHash():
    hash= request.form['data']
    db = TinyDB('db/blk.json')
    lst = db.all()

    response = app.response_class(
        response=json.dumps({"status":"not find"}),
        status=404,
        mimetype='application/json'
        )
    for i in lst:
        data = sha256(((i["Block Header"]['Version']).to_bytes(4, "little") +
            binascii.unhexlify(i["Block Header"]['Previous Block Hash']) +
            binascii.unhexlify(i["Block Header"]['Merkle Root']) +
            (i["Block Header"]['Timestamp']).to_bytes(4, "little") +
            (binascii.unhexlify(i["Block Header"]["Difficulty Target"])[::-1]) +
            (i["Block Header"]['Nonce']).to_bytes(4, "little"))).hexdigest()
        if data == hash:
            response = app.response_class(
                response=json.dumps(i),
                status=200,
                mimetype='application/json'
                )
            break;
    return response
