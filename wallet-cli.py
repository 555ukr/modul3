import sys
import requests
sys.path.insert(0, 'src/')
from transaction import Transaction
import cmd
import json
import os.path
from serializer import Serializer, Deserializer
from wallet import make_private_key, make_bitcoin_address, from_WIF_to_private, make_public_key
from pending_pool import accept_transaction, save_mempool
from termcolor import colored
import blockcypher
from script import execute
from tinydb import TinyDB, Query
import base58
import io
from contextlib import redirect_stdout

class HelloWorld(cmd.Cmd):
    prompt = colored('wallet-cli> ', "blue")
    intro = colored("Welcome to wallet cli!", "yellow")

    def do_EOF(self, line):
        return True

    def do_new(self, line):
        private = make_private_key()
        pbl = make_public_key(private)
        if (line == '-testnet'):
            address = make_bitcoin_address(pbl, net="test")
        else:
            address = make_bitcoin_address(pbl)
        f = open("address", "a")
        f.write(address + '\n')
        print("Bitcoin addr: ", address)
        print("Private key: ", private)
        db = TinyDB('db/addr.json')
        db.insert({"addr": address})

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
        db = TinyDB('db/addr.json')
        db.insert({"addr": address})

    def do_send(self, line):
        param = line.split(" ")
        if len(param) != 2 or param[0] == "-help":
            print("usage: send <address> <amount>")
            return
        trans = Transaction(param[0], param[1])
        if trans.status == 'KO':
            print(colored("*" * 50 + "\n\n" + " " * 4 + "ERROR (Wrong bitcoin addres or amount)" + "\n\n" + "*" * 50, 'red'))
            return
        # trans.display()
        lock = trans.param['tx_in'][0]['Signature Script']
        seri = Serializer(trans, sign=True)
        str = seri.make()
        trans.signFirst = str
        # print(trans.param['tx_in'][0]['Script Length'])
        if not trans.real_sign():
            print("\033[0m\033[91m" + "*" * 50 + "\n\n" + " " * 14 + "ERROR (Wrong private key)" + "\n\n" + "*" * 50 + "\033[0m")
            return
        unlock = trans.param['tx_in'][0]['Signature Script']
        if not execute(unlock + lock , str):
            print(colored("*" * 50 + "\n\n" + " " * 20 + "Script ERROR" + "\n\n" + "*" * 50, 'red'))
            return
        seri_sign = Serializer(trans)
        # print(trans.param)
        # print('____________________')
        final = seri_sign.make()
        # obk = Deserializer(final)
        # obk.make()
        # print(obk.param)
        tmp = ""
        for i in range(1, len(final) + 1):
            tmp = tmp + final[i - 1]
            if i % 49 == 0:
                tmp = tmp + "\n"
        print(colored("*" * 50 + "\n\n" + " " * 14 + "Serialized transaction\n\n" + tmp + "\n\n" + "*" * 50, 'green'))
        self.broadcast = final

    def do_broadcast(self, line):
        param = line.split(" ")
        if len(param) > 1 or param[0] == '-help':
            print("usage: broadcast [-testnet (optional)]")
            return
        if  not hasattr(self, 'broadcast'):
            print("usege: call send before broadcast")
            return
        if (param[0] == "-testnet"):
            API_KEY = "3e10e111bbcc4c6e8fb7fc9baafb564e"
            check = blockcypher.pushtx(tx_hex = self.broadcast, coin_symbol='btc-testnet', api_key = API_KEY)
            if 'tx' in check:
                print("Broadcast succesfull tx_hex: %" % check['tx']['hash'], "yellow")
            elif 'error' in check:
                print(colored(check['error'], 'red'))
            else:
                print(check)
        else:
            url = "http://127.0.0.1:5000/transaction"
            data = {'data': self.broadcast}
            r = requests.post(url, data)
            if r.status_code == 200:
                print(colored("Broadcast succesfull", "yellow"))
            else:
                print(colored("Broadcast fail", "red"))
    def do_exit(self, inp):
            # '''exit the application.'''
        print(colored("\nBye for now", "yellow"))
        return True

    def do_getBalance(self, line):
        res = 0
        db = TinyDB('db/addr.json')
        addr = db.all()
        for i in addr:
            i['addr'] = (base58.b58decode(bytes(i['addr'], encoding = 'utf-8'))[1:-4].hex())
            i['addr'] = ('76' + 'a9' + format(int(len(i['addr']) / 2), 'x') + i['addr'] +
                          '88' + 'ac')
        db = TinyDB('db/utxo.json')
        for i in addr:
            Utxo = Query()
            tmp = db.search(Utxo.Public_Script == i['addr'])
            if len(tmp) != 0:
                for y in tmp:
                    res = res + int(y['value'])
        print(res)

    def do_test(self,line):
        f = io.StringIO()
        g = io.StringIO()
        h = io.StringIO()
        print(colored("Test 'new'", "yellow"))
        with redirect_stdout(f):
            self.do_new("")
        print(colored("ok", "green"))
        print(colored("Test 'getBalance'", "yellow"))
        with redirect_stdout(g):
            self.do_getBalance("")
        balance = g.getvalue().rstrip()
        if (balance == "5000000000"):
            print(colored("ok", "green"))
        else:
            print(colored("ko", "red"))
        print(colored("Test 'broadcast'", "yellow"))
        with redirect_stdout(h):
            self.do_broadcast("")
        brd = h.getvalue().rstrip()
        if (brd == "usege: call send before broadcast"):
            print(colored("ok", "green"))
        else:
            print(colored("ko", "red"))

    do_EOF = do_exit

if __name__ == '__main__':
    HelloWorld().cmdloop()
