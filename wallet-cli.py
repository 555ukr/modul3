import sys
import requests
sys.path.insert(0, 'src/')
from transaction import Transaction
import cmd
import json
import os.path
from serializer import Serializer, Deserializer
from tx_validator import run_all
from wallet import make_private_key, make_bitcoin_address, from_WIF_to_private, signature,  make_public_key
from pending_pool import accept_transaction, save_mempool
from termcolor import colored

class HelloWorld(cmd.Cmd):
    prompt = colored('wallet-cli> ', "blue")
    intro = colored("Welcome to wallet cli!", "yellow")

    def do_EOF(self, line):
        return True

    def do_new(self, line):
        private = make_private_key()
        pbl = make_public_key(private)
        print(pbl)
        if (line == '-testnet'):
            address = make_bitcoin_address(pbl, net="test")
        else:
            address = make_bitcoin_address(pbl)
        f = open("address", "a")
        f.write(address + '\n')
        print("Bitcoin addr: ", address)
        print("Private key: ", private)

    def do_import(self, line):
        if not os.path.isfile(line):
            print("wrong path")
            return
        f = open(line, "r")
        wif = f.readline().strip()
        private = from_WIF_to_private(wif)
        address = make_bitcoin_address(private)
        f = open("address", "a")
        f.write(address + '\n')
        print("Private key: ", private)

    def do_send(self, line):
        param = line.split(" ")
        if len(param) != 2 or param[0] == "-help":
            print("usage: send <address> <amount>")
            return
        trans = Transaction(param[0], param[1])
        # trans.display()
        seri = Serializer(trans, sign=True)
        str = seri.make()
        trans.signFirst = str
        # print(trans.param['tx_in'][0]['Script Length'])
        trans.real_sign()
        # trans_sign.display()
        seri_sign = Serializer(trans)
        final = seri_sign.make()
        print(final)
        self.broadcast = final
        # if (not run_all({
        #     'sender': addres,
        #     'recipient': param[0],
        #     'coins': format(int(param[1]), 'x'),
        #     'public': pbl.hex(),
        #     'signature': sign,
        # })):
        #     print("Wrong parametes from send command")
        #     return
        # obj = Serializer(str(param[1]), addres, param[0], pbl.hex(), sign)
        # print("serialized transaction: ", obj.make())
        # status, data = accept_transaction(obj.make())
        # save_mempool(data)
        # if (status):
        #     print("Transaction saved to mem pool")
        # else:
        #     print("Transaction dosen't saved to mem pool")

    def do_broadcast(self, line):
        param = line.split(" ")
        if len(param) > 1 or param[0] == '-help':
            print("usage: broadcast [-testnet (optional)]")
            return
        if  not hasattr(self, 'broadcast'):
            print("usege: call send before broadcast")
            return
        url = "http://127.0.0.1:5000/transaction"
        data = {'data': self.broadcast}
        r = requests.post(url, data)

    def do_exit(self, inp):
            # '''exit the application.'''
        print(colored("\nBye for now", "yellow"))
        return True

    do_EOF = do_exit
if __name__ == '__main__':
    HelloWorld().cmdloop()
