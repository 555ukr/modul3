import time
from hashlib import sha256
from pending_pool import get_tree_trans
from merkle import prepare_data
from transaction import CoinbaseTransaction

class Block:

    def __init__(self, previous_hash):
        self.timestamp = int(time.time())
        self.nonce = 0
        self.previous_hash = previous_hash
        coinbase = CoinbaseTransaction()
        sgn, pbl = coinbase.signT()
        self.trans = get_tree_trans()
        self.hashTree = prepare_data(self.trans.copy())

    def valid(self):
        for i in range(len(self.trans)):
            self.trans[i]['coins'] = format(self.trans[i]['coins'], 'x')
            if not run_all(self.trans[i]):
                return False
        return True

    def hashBlock(self):
        data = sha256(bytes(str(self.timestamp) + str(self.nonce) +
            self.previous_hash + self.hashTree, 'utf-8')).hexdigest()
        return data
