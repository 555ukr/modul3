import hashlib
from hashlib import sha256
import binascii
from tx_validator import validate_signature

def execute(str, msg):
    lifo = []
    #hash160, checksig, dup, equalverify
    listComm = ['a9', 'ac', '76', '88']

    comm = parse(str, listComm)
    for i in range(len(comm)):
        if comm[i] in listComm:
            if execComm(lifo, comm[i], msg) == False:
                return False
        else:
            lifo.append(comm[i])
    if (len(lifo) != 1 or lifo[0] == False):
        return False
    return True


def execComm(lifo, comm, msg):
    if comm == '76':
        elm = lifo[-1]
        lifo.append(elm)
    elif comm == '88':
        first  = lifo.pop(-1)
        second = lifo.pop(-1)
        if first != second:
            return False
    elif comm == 'ac':
        pubKey = lifo.pop(-1)
        signature = lifo.pop(-1)
        lifo.append(validate_signature(signature, pubKey, msg))
    elif comm == 'a9':
        elm = lifo.pop(-1)
        sha1 = sha256(binascii.unhexlify(elm)).hexdigest()
        ripemd = hashlib.new('ripemd160', binascii.unhexlify(sha1)).hexdigest()
        lifo.append(ripemd)
    return True


def splitBypair(str):
    res = []
    tmp = ''

    if (len(str) % 2 != 0):
        return ['error']
    for ind, c  in enumerate(str):
        if ind % 2 != 0:
            res.append(tmp + c)
        else:
            tmp = c
    return res

def parse(str, listComm):
    arr = splitBypair(str)
    res = []
    i = 0

    while(1):
        if (i == len(arr)):
            break
        if arr[i] in listComm:
            res.append(arr[i])
        else:
            val = int(arr[i], 16)
            tmp = ""
            i = i + 1
            for y in range(val):
                tmp = tmp + arr[i + y]
            res.append(tmp)
            i = i + y
        i = i + 1
    return res

# unlock = "483045022100f46d9e19f5195820c0c8f5924918ce63d28518dfffcb6cfd830410296c29f89e0220311418092f860159c530abdb66fe44ed09e80495dc0da88a316c7f452a02f890012103387a90c1051d0fb0c68e9a313e34e27b085e445fd371420d4be08a8974d500b0"
# lock = "76a9147552068c8d10feb28dc163d5fbdde23e2932218d88ac"
# msg_R = "01000000019c3b7b71587f3496f1f05c0bff014e1c32817be800c3ca9604bae779ab4e8458010000001976a9147552068c8d10feb28dc163d5fbdde23e2932218d88acffffffff0250c30000000000001976a914c13e315661793e54a8f667d57213de804246801588ace0570e00000000001976a91470085ae0dc5c978f533599f6892408e1c684478488ac0000000001000000"
# re = execute(unlock + lock, msg_R)
# print(re)
# execute("48304502207470cf88ef1919fa30e8083bfff4466b10e7f739482fe35f0707fff512e86792022100d0a02961e55fced9e80ad79e7f705e2bbedcb3288a5644ca278c893a525badae0140e5613ad89d231fb48badf8fa0cef52be9285fa6fa3fb1b72369f2c760e811981abd1d51bfe7a783238181f98dfde3f712b96ca89af4f6b5b977b10a2fd8885be")
