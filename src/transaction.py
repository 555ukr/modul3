from hashlib import sha256
from wallet import make_bitcoin_address, from_WIF_to_private, sign_trans, make_addr_privKey
from tx_validator import validate_addr
import binascii
import os
import time
from tinydb import TinyDB, Query
import sys
import base58
from termcolor import colored

class Transaction:

    #pvlList ['bitcoin addr': "privat key", ...]
    #recipient bitcoin addr base58
    #recipient int

    def __init__(self, recipient, amount, signFirst="none"):
        self.signFirst = signFirst
        self.fee = 10000
        self.rest = False
        #init db
        if (len(recipient) > 35 or len(recipient) < 26 or not self.is_number(amount) or
                 not validate_addr(recipient)):
            self.status =  "KO"
            return
        self.db = TinyDB('db/wallet.json')
        amount = str(int(float(amount) * (10 ** 8)))

        #make list of input and output
        status_in, tx_in = self.make_in(amount)
        status_out, tx_out = self.make_out(recipient, amount)
        if (status_out == False or status_in == False):
            self.status =  "KO"
            return
        self.param = {
            'vertion': 1,
            'tx_in count': len(tx_in),
            'tx_in': tx_in,
            'tx_out count': len(tx_out),
            'tx_out': tx_out,
            'lock_time': 0
        }
        self.status = "OK"

    def make_out(self, recipient, amount):
        all_addr = self.db.all()
        sum = 0
        for i in range(len(all_addr)):
            sum = sum + int(all_addr[i]['coins'])
        rest = int(sum) - int(amount) - self.fee
        if (rest < 0):
            return False, 'error'
        decode_recip = (base58.b58decode(bytes(recipient, encoding = 'utf-8'))[1:-4].hex())
        script_pay = ('76' + 'a9' + format(int(len(decode_recip) / 2), 'x') + decode_recip +
                         '88' + 'ac')

        tx_out = [{
            'value': amount,
            'Script Length': int(len(script_pay) / 2),
            'Public Script': script_pay
        }]
        if rest != 0:
            self.rest = True
            addr, prv = make_addr_privKey(net="test")
            self.restAddr = addr
            self.restPrv = prv

            decode_addr = (base58.b58decode(bytes(addr, encoding = 'utf-8'))[1:-4].hex())
            script_pay = ('76' + 'a9' + format(int(len(decode_addr) / 2), 'x') + decode_addr +
                            '88' + 'ac')
            tx_out.append({
                'value': rest,
                'Script Length': int(len(script_pay) / 2),
                'Public Script': script_pay,
            })
            # if rest is exesist
            # self.db.insert({
            #     'address': addr,
            #     'coins': 0
            # })
        return True, tx_out

    def make_in(self, amount):
        all_addr = self.db.all()
        sum = 0
        for i in range(len(all_addr)):
            sum = sum + int(all_addr[i]['coins'])
        rest = int(sum) - int(amount)
        if (rest < 0):
            return False, 'error'
        list_tx_in = []
        for i in range(len(all_addr)):
            if (all_addr[i]['coins'] != 0):
                script_in = all_addr[i]['prev_publ_key']
                list_tx_in.append({
                    "Previous txid": all_addr[i]['prev_tx'],
                    "Previous Tx Index": all_addr[i]['prev_tx_ind'],
                    "Script Length": int(len(script_in) / 2),
                    "Signature Script": script_in,
                    "Sequence": "ffffffff"
                })
        return True, list_tx_in

    def real_sign(self):
        signHash = "01"
        all_addr = self.db.all()
        for i in range(len(self.param['tx_in'])):
            prv = input("\033[92mEnter private key for %s: \033[93m" % all_addr[i]['address'])
            if (len(prv) != 64 or not self.is_hex(prv)):
                return False
            sign, pbl = sign_trans(self.signFirst, prv)
            script_in = format(int(len(sign + signHash) / 2), 'x') + sign + signHash + format(int(len(pbl) / 2), 'x') + pbl
            self.param['tx_in'][i]['Script Length'] = int(len(script_in) / 2)
            self.param['tx_in'][i]['Signature Script'] = script_in
        return True

    def displayRest():
        if self.rest:
            print(colored("Rest was retert to address: %s\nPrivate key(pls, remember): %s" % (self.restAddr, self.restPrv), "red"))


    def display(self):
        print("{'vertion':", self.param['vertion'], ",")
        print("'tx_in count':" ,self.param['tx_in count'], ",")
        print("'tx_in':")
        for i in range(len(self.param['tx_in'])):
            print("      {\n        'Previous txid':", self.param['tx_in'][i]['Previous txid'])
            print("        'Previous Tx Index':", self.param['tx_in'][i]['Previous Tx Index'])
            print("        'Script Length':", self.param['tx_in'][i]['Script Length'])
            print("        'Signature Script':", self.param['tx_in'][i]['Signature Script'])
            print("        'Sequence':", self.param['tx_in'][i]['Sequence'], "\n      },")
        print("'tx_out':")
        for i in range(len(self.param['tx_out'])):
            print("      {\n        'value':", self.param['tx_out'][i]['value'])
            print("        'Script Length':", self.param['tx_out'][i]['Script Length'])
            print("        'Public Script':", self.param['tx_out'][i]['Public Script'], "\n      },")
        print("}")

    def is_number(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def is_hex(self, str):
        try:
            int(str, 16)
            return True
        except ValueError:
            return False


class CoinbaseTransaction(Transaction):

    def __init__(self, recipient):
        amount = str(int(CoinbaseTransaction.getReword()))

        #make list output

        status_out, tx_out = self.make_out(recipient, amount)
        if (status_out == False):
            self.status =  "KO"
            return
        self.param = {
            'vertion': 1,
            'tx_in count': 1,
            'tx_in': [{
                "Previous txid": "0000000000000000000000000000000000000000000000000000000000000000",
                "Previous Tx Index": 4294967295,
                "Script Length": 69,
                "Signature Script": "03ec59062f48616f4254432f53756e204368756e2059753a205a6875616e67205975616e2c2077696c6c20796f75206d61727279206d653f2f06fcc9cacc19c5f278560300",
                "Sequence": "ffffffff"
            }],
            'tx_out count': 1,
            'tx_out': tx_out,
            'lock_time': 0
        }
        self.status = "OK"

    @staticmethod
    def getReword():
        db = TinyDB('db/blk.json')
        all = len(db.all())
        val = 50 * 10**8
        if (int(all / 5) != 0):
            tmp = int(all / 5)
            for i in range(tmp):
                val = int(val / 2)
        return val

    def make_out(self, recipient, amount):

        decode_recip = (base58.b58decode(bytes(recipient, encoding = 'utf-8')).hex())[2:-8]
        script_pay = ('76' + 'a9' + format(int(len(decode_recip) / 2), 'x') + decode_recip +
                         '88' + 'ac')
        tx_out = [{
            'value': amount,
            'Script Length': int(len(script_pay) / 2),
            'Public Script': script_pay
        }]
        return True, tx_out

# obj = CoinbaseTransaction('n3DpYpJ5vPZEJ5K6zGS5NWTD6Y2gy7699p')
# obj.display()

# print('_______________________________________________________________\n\n')
# obj = Transaction('1FKLHE97PBro3zyBxHU1AvfbLcWnyQ3jjU', "13")
# {
# '1FwyyY38DgARnpiGcgFYr1ccoMS3tXtcF5' : 'a17b7a301dc0ebfafecb6dad947435a53db940d23aa866412e8649eb13a08ac2',
# '12Ye1Hn8CmLayfyKneiCCsvvuRHgX8TghQ' : '4adc80ee46fd0521e4540f70ed5befd0a0152872fc2f75443fb0c30669178365'
# }
