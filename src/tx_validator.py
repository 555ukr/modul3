import sys
sys.path.insert(0, '../01/')
import base58
import binascii
from hashlib import sha256
from wallet import make_bitcoin_address
from ecdsa import VerifyingKey, SECP256k1, BadSignatureError

def validate_addr(addr):
    decode = base58.b58decode(bytes(addr, encoding = 'utf-8'))
    checksum = decode.hex()[-8:]
    check = decode.hex()[:-8]
    if (sha256(sha256(binascii.unhexlify(check)).digest()).hexdigest()[:8] != checksum):
        return False
    return True

def validate_addr_by_public(addr, public):
    if (public[:2] != '04'):
        ch_addr = make_bitcoin_address('04' + public)
    else:
        ch_addr = make_bitcoin_address(public)
    if (ch_addr != addr):
        return False
    return True

def validate_signature(signature, pbl, sender, recipient, amount):

    # format(int(amount), 'x') change couse amount is int
    st = sender + recipient + str(amount)
    message = sha256(bytes(st, 'utf-8')).hexdigest()

    vk = VerifyingKey.from_string(bytes.fromhex(pbl), curve=SECP256k1, hashfunc=sha256)
    try:
        vk.verify(binascii.unhexlify(signature), bytes(message, 'utf-8'))
        return True
    except BadSignatureError:
        return False

def run_all(dict):
    if (not validate_addr(dict['sender']) or not validate_addr(dict['recipient']) or
        not validate_addr_by_public(dict['sender'], dict['public'])):
        return False
    print(True)
    if not validate_signature(dict['signature'], dict['public'], dict['sender'], dict['recipient'], dict['coins']):
        return False
    return True

# tr = validate_signature('4a62841fce4ec74e5db72f091d46f38c4ee807e933a07c2782eeb145db24f638fe5570b2e49a9d107cb231a7c284368b51959eb9aa17ceeda9379f89412dfbac',
# '50863ad64a87ae8a2fe83c1af1a8403cb53f53e486d8511dad8a04887e5b23522cd470243453a299fa9e77237716103abc11a1df38855ed6f2ee187e9c582ba6',
# '15Uikr1EwQYS8zx7wAEfggExvDRinc4y5n', '1Hj3hALRJy3iFvLW6Koubb7Wc6WdsCTF1Y', '12')
#
# print(tr)

# pbl = '50863ad64a87ae8a2fe83c1af1a8403cb53f53e486d8511dad8a04887e5b23522cd470243453a299fa9e77237716103abc11a1df38855ed6f2ee187e9c582ba6'
# vk = VerifyingKey.from_string(bytes.fromhex(pbl), curve=SECP256k1)
# st = '15Uikr1EwQYS8zx7wAEfggExvDRinc4y5n' + '1Hj3hALRJy3iFvLW6Koubb7Wc6WdsCTF1Y' + '12'
# message = sha256(bytes(st, 'utf-8')).hexdigest()
# sig = '4a62841fce4ec74e5db72f091d46f38c4ee807e933a07c2782eeb145db24f638fe5570b2e49a9d107cb231a7c284368b51959eb9aa17ceeda9379f89412dfbac'
# try:
#     print(len(binascii.unhexlify(sig)))
#     vk.verify(binascii.unhexlify(sig), bytes(message, 'utf-8'))
#     print ("good signature")
# except BadSignatureError:
#     print ("BAD SIGNATURE")
