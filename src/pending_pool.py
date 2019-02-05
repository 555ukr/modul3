import sys
sys.path.insert(0, 'src/')
# from tx_validator import run_all
from serializer import Deserializer
from tinydb import TinyDB, Query

def accept_transaction(str):
    obj = Deserializer(str)
    obj.make()
    # if not run_all(data):
    #     return False, data
    return True, obj.param

def save_mempool(trans):
    db = TinyDB('db/mempoll.json')
    # trans['coins'] = int(trans['coins'], 16)
    db.insert(trans)
    # print(db.all()[-1:])

def get_tree_trans():
    db = TinyDB('db/mempoll.json')
    return db.all()[-3:]
