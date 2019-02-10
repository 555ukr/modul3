from tinydb import TinyDB, Query
from serializer import Serializer
from merkle import Param
import binascii
from hashlib import sha256

def updateUTXO():
    db = TinyDB('db/blk.json')
    lstBlk = (db.all()[-1:])[0]['Transactions']
    dlt = []
    apd = []
    for i in lstBlk:
        tmp = Param(i)
        obj = Serializer(tmp)
        seri = obj.make()
        hash = (sha256(sha256(binascii.unhexlify(seri)).digest()).digest()[::-1]).hex()
        for y in i['tx_in']:
            if y['Previous txid'] != "0000000000000000000000000000000000000000000000000000000000000000":
                dlt.append({
                    'txid': y['Previous txid'],
                    'index': y['Previous Tx Index']
                })
        g = 0
        for z in i['tx_out']:
            apd.append({
                'value': z['value'],
                'txid': hash,
                'index': g,
                'Public_Script': z['Public Script']
            })
            g = g + 1
    deleteUTXO(dlt)
    appendUTXO(apd)

def deleteUTXO(arr):
    db = TinyDB('db/utxo.json')
    for i in arr:
        utxo = Query()
        res = db.search(utxo.txid == i['txid'] and utxo.index == i['index'])
        if len(res) != 0:
            db.remove(utxo.txid == i['txid'] and utxo.index == i['index'])

def appendUTXO(arr):
    db = TinyDB('db/utxo.json')
    for i in arr:
        db.insert(i)

def restartUTXO():
    db = TinyDB('db/utxo.json')
    db.purge()
    updateUTXO()
