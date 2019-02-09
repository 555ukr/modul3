import sys
sys.path.insert(0, '../01/')
import base58
import binascii
from hashlib import sha256
from wallet import make_bitcoin_address, getFullPubKeyFromCompressed
from ecdsa import VerifyingKey, SECP256k1, BadSignatureError
import ecdsa

def validate_addr(addr):
    decode = base58.b58decode(bytes(addr, encoding = 'utf-8'))
    checksum = decode.hex()[-8:]
    check = decode.hex()[:-8]
    if (sha256(sha256(binascii.unhexlify(check)).digest()).hexdigest()[:8] != checksum):
        return False
    return True

def validate_signature(signature, public, message):
    pbl = getFullPubKeyFromCompressed(binascii.unhexlify(public))
    key = ecdsa.VerifyingKey.from_string(pbl[1:], ecdsa.SECP256k1)
    try:
        return key.verify_digest(binascii.unhexlify(signature[:-2]), sha256(sha256(binascii.unhexlify(message)).digest()).digest(), sigdecode = ecdsa.util.sigdecode_der)
    except ecdsa.BadSignatureError:
        return False
