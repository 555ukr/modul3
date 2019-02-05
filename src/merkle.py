from hashlib import sha256
import binascii
from serializer import Serializer

def prepare_data(arr):
    for i in range(len(arr)):
        obj = Serializer(arr[i]['coins'], arr[i]['sender'], arr[i]['recipient'], arr[i]['public'], arr[i]['signature'])
        arr[i] = obj.make()
    return make_tree(arr)

def make_tree(hashArr):
    tmp = list()

    if (len(hashArr) == 1):
        return hashArr[0]
    elif len(hashArr) % 2 != 0:
        hashArr.append(hashArr[-1])
    for i in range(0, len(hashArr), 2):
        tmp.append(sha256(bytes(str(hashArr[i]) + str(hashArr[i + 1]), 'utf-8')).hexdigest())
    return make_tree(tmp)
