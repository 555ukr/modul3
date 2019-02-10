import time
from hashlib import sha256
from pending_pool import get_tree_trans
from merkle import prepare_data
from transaction import CoinbaseTransaction
import binascii
# from blockchain import Blockchain

class Block:

    def __init__(self, previous_hash, coinbase):
        self.prev_hash = previous_hash
        self.coinbase = coinbase
        self.nonce = 0

        self.trans = get_tree_trans()
        self.trans.insert(0, {
            "transaction": self.coinbase.param,
            "hash": ""
        })
        blockHeader = self.blockHeader()
        tmp = []
        for i in self.trans:
            tmp.append(i['transaction'])
        self.param = {
            'Block Size': "ffffffff",
            "Block Header": blockHeader,
            "Transaction Counter": len(tmp),
            "Transactions": tmp
        }

    def blockHeader(self):
        tree = prepare_data(self.trans.copy())
        target = self.calculateTagret()
        self.header = {
            "Version": 1,
            "Previous Block Hash": self.prev_hash,
            "Merkle Root": tree,
            "Timestamp": int(time.time()),
            "Difficulty Target": target,
            "Nonce": self.nonce
        }
        return self.header

    def calculateTagret(self):
        return "2003a30c"

    def hashBlock(self):
        data = sha256(((self.header['Version']).to_bytes(4, "little") +
            binascii.unhexlify(self.header['Previous Block Hash']) +
            binascii.unhexlify(self.header['Merkle Root']) +
            (self.header['Timestamp']).to_bytes(4, "little") +
            (binascii.unhexlify(self.header["Difficulty Target"])[::-1]) +
            (self.header['Nonce']).to_bytes(4, "little"))).hexdigest()
        return data

# cn = CoinbaseTransaction('mnKt5wEPTDafet1yGFwcLwr91m6pXVJeh2')
# print("*************")
# obj = Block("0000000000000000000000000000000000000000000000000000000000000000", cn)
# nonce, hash = Blockchain.mine(obj)
# print(obj.param)
# print('____________________')
# print(nonce)
# print(hash)
