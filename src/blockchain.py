# from block import Block
from pending_pool import accept_transaction, save_mempool
from transaction import CoinbaseTransaction
from tinydb import TinyDB, Query
from serializer import Serializer

class Blockchain:

    @staticmethod
    def mine(dfc, blk):
        while(1):
            tmp = blk.hashBlock()
            if (tmp[:dfc] == ('0' * dfc)):
                break
            blk.nonce = blk.nonce + 1
        return blk.nonce, tmp

    @staticmethod
    def submit_tx(new):
        status, data = accept_transaction(new)
        if (status):
            if save_mempool(data):
                print("127.0.0.1 --- new transaction saved to mem pool")
                return True
        else:
            print("127.0.0.1 --- wrong transaction")
        return False

    @staticmethod
    def genesis_block():
        genesis = CoinbaseTransaction("mnKt5wEPTDafet1yGFwcLwr91m6pXVJeh2")
        seri = Serializer(genesis)
        str = seri.make()
        
        db = TinyDB('db/blk.json')
        db.purge()


    @staticmethod
    def add_node(node):
        db = TinyDB('nodelist/nodedb.json')
        db.insert(node)
