import secrets
import binascii
import base58
import hashlib
from hashlib import sha256
from ecdsa import SigningKey, SECP256k1, util
from ecdsa.util import string_to_number, number_to_string
from ecdsa.curves import SECP256k1
import ecdsa

# function generate private key to file
def generateFile():
    f = open("privetKey", "w")
    f.write(secrets.token_hex(32))

# convert public key to WIF
def generateWIF(ky):
    key = '80' + ky

    shaFirst = sha256(binascii.unhexlify(key)).hexdigest()
    shaSecond = (sha256(binascii.unhexlify(shaFirst)).hexdigest())
    final = base58.b58encode(binascii.unhexlify(key + shaSecond[0:8])).decode("utf-8")
    return (final)

def make_public_key(key):
    private = SigningKey.from_string(binascii.unhexlify(key), curve=SECP256k1)
    public = private.get_verifying_key()
    final = '04' + public.to_string().hex()
    return final

def make_bitcoin_address(pbl, net="main"):
    pbl = public_to_compressed(pbl)
    netw = '00' if net == "main" else '6f'
    sha1 = sha256(binascii.unhexlify(pbl)).hexdigest()
    ripemd = hashlib.new('ripemd160', binascii.unhexlify(sha1)).hexdigest()
    network = netw + ripemd
    coupleSha = sha256(binascii.unhexlify(sha256(binascii.unhexlify(network)).hexdigest())).hexdigest()
    final = base58.b58encode(binascii.unhexlify(network + coupleSha[0:8])).decode("utf-8")
    return (final)


# def signature(msg, key):
#     private = SigningKey.from_string(binascii.unhexlify(key), curve=SECP256k1, hashfunc=sha256)
#     public = private.get_verifying_key()
#     signature = private.sign(msg.encode('utf-8'), hashfunc=sha256, sigencode=util.sigencode_der)
#     return signature.hex(), (public.to_string()).hex()
    # sk = ecdsa.SigningKey.from_string(pk_bytes, curve=ecdsa.SECP256k1)

def sign_trans(msg, ky):
    key = base58.b58decode_check(generateWIF(ky))[1:33].hex()
    hashed_tx_to_sign = hashlib.sha256(hashlib.sha256(binascii.unhexlify(msg)).digest()).digest()
    private = SigningKey.from_string(binascii.unhexlify(key), curve=ecdsa.SECP256k1)
    public =  private.get_verifying_key()
    public = public_to_compressed('04' + (public.to_string()).hex())
    # print("priv------ ", key)
    # print("----hash ", hashed_tx_to_sign.hex())
    signature = private.sign_digest(hashed_tx_to_sign, sigencode=ecdsa.util.sigencode_der_canonize)
    return signature.hex(), public


def make_private_key():
    return secrets.token_hex(32)

def from_WIF_to_private(wif):
    decode = base58.b58decode(bytes(wif, encoding = 'utf-8'))
    checksum = decode[-4:]
    firstSha = sha256(binascii.unhexlify(decode[:-4].hex())).hexdigest()
    secondSha = sha256(binascii.unhexlify(firstSha)).hexdigest()
    assert secondSha[:8] == checksum.hex()
    return secondSha

def make_addr_privKey(net="main"):
    prv = make_private_key()
    pbl = make_public_key(prv)
    addr = make_bitcoin_address(pbl, net)
    return addr, prv

def public_to_compressed(pubkey):
    tmp = binascii.unhexlify(pubkey[2:])
    pbl = tmp[: int(len(tmp) / 2)]
    if tmp[-1] % 2:
        pbl = b'\x03' + pbl
    else:
        pbl = b'\x02' + pbl
    return pbl.hex()

def getFullPubKeyFromCompressed(comp_key:  bytearray) -> bytes:
    x = int.from_bytes(comp_key[1:], byteorder='big')
    is_even = True if comp_key[1] == '2' else False
    """ Derive y point from x point """
    curve = ecdsa.SECP256k1.curve
    # The curve equation over F_p is:
    #   y^2 = x^3 + ax + b
    a, b, p = curve.a(), curve.b(), curve.p()
    alpha = (pow(x, 3, p) + a * x + b) % p
    beta = ecdsa.numbertheory.square_root_mod_prime(alpha, p)
    if (beta % 2) == is_even:
        beta = p - beta
    return bytearray.fromhex( f"04{x:064x}{beta:064x}")
