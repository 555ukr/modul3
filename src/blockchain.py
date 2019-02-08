from block import Block
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
        genesis = CoinbaseTransaction()
        db = TinyDB('mempoll/db.json')
        db.purge()
        sgn, pbl = genesis.signT()
        dic = {
            "coins": genesis.amount,
             "sender": genesis.sender,
             "recipient": genesis.recipient,
             "public": pbl.hex(),
             "signature": sgn
            }
        save_mempool(dic)
        blk = Block("0000000000000000000000000000000000000000000000000000000000000000")
        nonce, hash = Blockchain.mine(1, blk)
        db = TinyDB('blocks/blk.json')
        db.purge()
        db.insert({
            'index': 1,
            'nonce': nonce,
            'hash': hash,
            'timestamp': blk.timestamp,
            'previous_hash': blk.previous_hash,
            'tranasaction': blk.trans
        })

    @staticmethod
    def add_node(node):
        db = TinyDB('nodelist/nodedb.json')
        db.insert(node)
