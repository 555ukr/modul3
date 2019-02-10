from hashlib import sha256
import binascii
from serializer import Serializer

class Param:
    def __init__(self, param):
        self.param = param

def prepare_data(arr):
    for i in range(len(arr)):
        tmp = Param(arr[i]['transaction'])
        obj = Serializer(tmp)
        arr[i] = obj.make()
    return make_tree(arr)

def make_tree(hashArr):
    tmp = list()

    if (len(hashArr) == 1):
        if (len(hashArr[0]) != 64):
            return sha256(binascii.unhexlify(hashArr[0])).hexdigest()
        return hashArr[0]
    elif len(hashArr) % 2 != 0:
        hashArr.append(hashArr[-1])
    for i in range(0, len(hashArr), 2):
        tmp.append(sha256(binascii.unhexlify(str(hashArr[i]) + str(hashArr[i + 1]))).hexdigest())
    return make_tree(tmp)
