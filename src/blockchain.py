from block import Block
from pending_pool import accept_transaction, save_mempool
from transaction import CoinbaseTransaction
from tinydb import TinyDB, Query
from serializer import Serializer
import binascii
from hashlib import sha256

class Blockchain:

    @staticmethod
    def mine(blk):
        bits = int(blk.param['Block Header']['Difficulty Target'], 16)
        exp = bits >> 24
        mant = bits & 0xffffff
        target_hexstr = '%064x' % (mant * (1 << (8 * (exp - 3))))
        while(1):
            tmp = blk.hashBlock()
            if tmp < target_hexstr:
                break
            blk.param['Block Header']['Nonce'] = blk.param['Block Header']['Nonce'] + 1
        return blk.param['Block Header']['Nonce'], tmp

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
        genesis = {
            'Block Size': 'ffffffff',
            'Block Header':
                {
                    'Version': 1,
                    'Previous Block Hash': '0000000000000000000000000000000000000000000000000000000000000000',
                    'Merkle Root': 'd56ee5da68a7f99201234654e6d0672fa4916a008399322d4d912d08c39bf9a2',
                    'Timestamp': 1549807035,
                    'Difficulty Target': '2003a30c',
                    'Nonce': 33
                },
                'Transaction Counter': 1,
                'Transactions': [{
                    'vertion': 1,
                    'tx_in count': 1,
                    'tx_in': [{
                        'Previous txid': '0000000000000000000000000000000000000000000000000000000000000000',
                        'Previous Tx Index': 4294967295,
                        'Script Length': 69,
                        'Signature Script': '03ec59062f48616f4254432f53756e204368756e2059753a205a6875616e67205975616e2c2077696c6c20796f75206d61727279206d653f2f06fcc9cacc19c5f278560300',
                        'Sequence': 'ffffffff'
                        }],
                    'tx_out count': 1,
                    'tx_out': [{
                        'value': '5000000000',
                        'Script Length': 25,
                        'Public Script': '76a9144ab0ca9d78ca14fc90f6227d46ba1a8fa2f96b0688ac'
                        }],
                    'lock_time': 0
                    }]}
        db = TinyDB('db/blk.json')
        db.purge()
        db.insert(genesis)

    @staticmethod
    def newBlock():
        f = open("resources/minerkey", "r")
        key = (f.readline()).rstrip()
        coinbase = CoinbaseTransaction(key)

        db = TinyDB('db/blk.json')
        all = db.all()[-1:]
        data = sha256(((all[0]["Block Header"]['Version']).to_bytes(4, "little") +
                binascii.unhexlify(all[0]["Block Header"]['Previous Block Hash']) +
                binascii.unhexlify(all[0]["Block Header"]['Merkle Root']) +
                (all[0]["Block Header"]['Timestamp']).to_bytes(4, "little") +
                (binascii.unhexlify(all[0]["Block Header"]["Difficulty Target"])[::-1]) +
                (all[0]["Block Header"]['Nonce']).to_bytes(4, "little"))).hexdigest()
        obj = Block(data, coinbase)
        nonce, hash = Blockchain.mine(obj)
        db.insert(obj.param)

    @staticmethod
    def add_node(node):
        db = TinyDB('nodelist/nodedb.json')
        db.insert(node)
