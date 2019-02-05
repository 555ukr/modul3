import hashlib
from hashlib import sha256
import binascii

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
        pass
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

# re = execute("47304402200aa5891780e216bf1941b502de29890834a2584eb576657e340d1fa95f2c0268022010712e05b30bfa9a9aaa146927fce1819f2ec6d118d25946256770541a8117b6012103d2305c392cbd5ac36b54d3f23f7305ee024e25000f5277a8c065e12df503592676a9143bbebbd7a3414f9e5afebe79b3b408bada63cde288ac", "LOL")
# print(re)
# execute("48304502207470cf88ef1919fa30e8083bfff4466b10e7f739482fe35f0707fff512e86792022100d0a02961e55fced9e80ad79e7f705e2bbedcb3288a5644ca278c893a525badae0140e5613ad89d231fb48badf8fa0cef52be9285fa6fa3fb1b72369f2c760e811981abd1d51bfe7a783238181f98dfde3f712b96ca89af4f6b5b977b10a2fd8885be")
