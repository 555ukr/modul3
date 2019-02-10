import cmd
import sys
from termcolor import colored
sys.path.insert(0, 'src/')
from blockchain import Blockchain
from tinydb import TinyDB, Query
from hashlib import sha256
import binascii

class HelloWorld(cmd.Cmd):
    prompt = colored('mining-cli> ', "blue")

    def preloop(self):
        print(colored("Welcome to miner cli!", "yellow"))
        if (len(sys.argv) > 1 and sys.argv[1] == '-restart'):
            Blockchain.genesis_block()
            print(colored('Genesis block created', "cyan"))

    def do_EOF(self, line):
        return True

    def do_getBlockchainLength(self, line):
        db = TinyDB('db/blk.json')
        length = len(db.all())
        print(length)

    def do_getBlockchainHash(self, line):
        db = TinyDB('db/blk.json')
        all = db.all()
        y = 1
        for i in all:
            data = sha256(((i["Block Header"]['Version']).to_bytes(4, "little") +
                binascii.unhexlify(i["Block Header"]['Previous Block Hash']) +
                binascii.unhexlify(i["Block Header"]['Merkle Root']) +
                (i["Block Header"]['Timestamp']).to_bytes(4, "little") +
                (binascii.unhexlify(i["Block Header"]["Difficulty Target"])[::-1]) +
                (i["Block Header"]['Nonce']).to_bytes(4, "little"))).hexdigest()
            print(colored("Block number %i has hash %s" % (y, data), "yellow"))
            y = y + 1

    def do_mineNew(self, line):
        Blockchain.newBlock()
        print(colored("New block add to blockchain", "yellow"))

    def do_exit(self, inp):
            # '''exit the application.'''
        print(colored("\nBye for now", "yellow"))
        return True

    do_EOF = do_exit

if __name__ == '__main__':
    HelloWorld().cmdloop()
