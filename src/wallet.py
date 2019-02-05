import secrets
import binascii
import base58
import hashlib
from hashlib import sha256
from ecdsa import SigningKey, SECP256k1, util

# function generate private key to file
def generateFile():
    f = open("privetKey", "w")
    f.write(secrets.token_hex(32))

# convert public key to WIF
def generateWIF():
    f = open("privetKey", "r")
    key = '80' + f.readline().strip()

    shaFirst = sha256(binascii.unhexlify(key)).hexdigest()
    shaSecond = (sha256(binascii.unhexlify(shaFirst)).hexdigest())
    final = base58.b58encode(binascii.unhexlify(key + shaSecond[0:8])).decode("utf-8")
    print(final)

def make_public_key(key):
    private = SigningKey.from_string(binascii.unhexlify(key), curve=SECP256k1)
    public = private.get_verifying_key()
    final = '04' + public.to_string().hex()
    return final

def make_bitcoin_address(pbl, net="main"):
    netw = '00' if net == "main" else '6F'
    sha1 = sha256(binascii.unhexlify(pbl)).hexdigest()
    ripemd = hashlib.new('ripemd160', binascii.unhexlify(sha1)).hexdigest()
    network = netw + ripemd
    coupleSha = sha256(binascii.unhexlify(sha256(binascii.unhexlify(network)).hexdigest())).hexdigest()
    final = base58.b58encode(binascii.unhexlify(network + coupleSha[0:8])).decode("utf-8")
    return (final)

def signature(msg, key):
    private = SigningKey.from_string(binascii.unhexlify(key), curve=SECP256k1, hashfunc=sha256)
    public = private.get_verifying_key()
    signature = private.sign(msg.encode('utf-8'), hashfunc=sha256, sigencode=util.sigencode_der)
    return signature.hex(), (public.to_string()).hex()

def make_private_key():
    return secrets.token_hex(32)

def from_WIF_to_private(wif):
    decode = base58.b58decode(bytes(wif, encoding = 'utf-8'))
    checksum = decode[-4:]
    firstSha = sha256(binascii.unhexlify(decode[:-4].hex())).hexdigest()
    secondSha = sha256(binascii.unhexlify(firstSha)).hexdigest()
    assert secondSha[:8] == checksum.hex()
    return secondSha

def make_addr_privKey():
    prv = secrets.token_hex(32)
    pbl = make_public_key(prv)
    addr = make_bitcoin_address(pbl)
    return addr, prv
