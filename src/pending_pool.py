import sys
sys.path.insert(0, 'src/')
from serializer import Deserializer
from tinydb import TinyDB, Query
from hashlib import sha256
import binascii

def accept_transaction(str):
    obj = Deserializer(str)
    obj.make()
    hash = sha256(binascii.unhexlify(str)).hexdigest()
    return (True, {
                    "transaction": obj.param,
                    "hash": hash
                    })

def save_mempool(trans):
    db = TinyDB('db/mempoll.json')
    dw = Query()
    res = db.search(dw.hash == trans['hash'])
    if (len(res) == 0):
        db.insert(trans)
        return True
    return False

def get_tree_trans():
    db = TinyDB('db/mempoll.json')
    return db.all()[-3:]
