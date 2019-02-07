import hashlib
import base58
import ecdsa
import struct
import binascii
from enum import Enum
from ecdsa.util import string_to_number, number_to_string
from ecdsa.curves import SECP256k1

CURVE_ORDER = SECP256k1.order
input_amount = 8462282
output_amount = 60000
fee = 50000
sender_address = "mh7jpHw8jEBZjx7j83diZ2XBtqjJ8GNTqv"
# sender_pub = "0488cd594b9f024e3866fb3960195f118be39b5e5a8f591b3b4c46777ebd6560dff20183e34a2693a4f583ef30a9d40b2a053f09469eff6ceb146c12c6c1b50256"
sender_compressed_pub = "02b3de1f9c1549a907af43e26117accadd0382d09a29f8304db9f3fd996e14d14c"
# sender_pub_bytes = bytes.fromhex(sender_pub)
sender_compressed_pub_bytes = bytes.fromhex(sender_compressed_pub)
sender_priv = "40760e3d3c4739f70f33edaa5c6b6ba0d8c56cddb0bee05e540176d7c247d833"
sender_wif_priv = "5JJg9xKTZ1CkqquWVWf3132pwxhR28FBZgHcRd4jHmJgZHQGGPg"
recipient_address = "n2A2QxKacSbpn5ii3r9dXUsyce2omGQZs8"
prev_txid = "c110b75c87d8e47e0027d8865fc68b0b20db62c3b63832be303b2359eae71fd9"

def ripemd160(x):
    d = hashlib.new('ripemd160')
    d.update(x)
    return d


class Network(Enum):
    TEST_NET = 0
    PROD_NET = 1


class raw_tx:
    version = struct.pack("<L", 1)
    tx_in_count = struct.pack("<B", 1)
    tx_in = {}  # TEMP
    tx_out_count = struct.pack("<B", 2)
    tx_out1 = {}  # TEMP
    tx_out2 = {}  # TEMP
    lock_time = struct.pack("<L", 0)


def flip_byte_order(string):
    flipped = "".join(reversed([string[i:i + 2] for i in range(0, len(string), 2)]))
    return flipped


def normalize_secret_bytes(privkey_bytes: bytes) -> bytes:
    scalar = string_to_number(privkey_bytes) % CURVE_ORDER
    if scalar == 0:
        raise Exception('invalid EC private key scalar: zero')
    privkey_32bytes = number_to_string(scalar, CURVE_ORDER)
    return privkey_32bytes

def make_raw_transaction():
    rtx = raw_tx()

    my_address = sender_address
    my_hashed_pubkey = base58.b58decode_check(my_address)[1:].hex()

    my_private_key = sender_wif_priv
    my_private_key_hex = base58.b58decode_check(my_private_key)[1:33].hex()
    print("private-----------", my_private_key_hex)
    print("private-----------", my_private_key)

    recipient = recipient_address
    recipient_hashed_pubkey = base58.b58decode_check(recipient)[1:].hex()

    my_output_tx = prev_txid
    input_value = input_amount

    # form tx_in
    rtx.tx_in["txouthash"] = bytes.fromhex(flip_byte_order(my_output_tx))
    rtx.tx_in["tx_out_index"] = struct.pack("<L", 0)
    rtx.tx_in["script"] = bytes.fromhex("76a914%s88ac" % my_hashed_pubkey)
    print("---->>>>>", my_hashed_pubkey)
    rtx.tx_in["scrip_bytes"] = struct.pack("<B", len(rtx.tx_in["script"]))
    rtx.tx_in["sequence"] = bytes.fromhex("ffffffff")

    # form tx_out
    rtx.tx_out1["value"] = struct.pack("<Q", output_amount)
    rtx.tx_out1["pk_script"] = bytes.fromhex("76a914%s88ac" % recipient_hashed_pubkey)
    rtx.tx_out1["pk_script_bytes"] = struct.pack("<B", len(rtx.tx_out1["pk_script"]))

    return_value = input_value - output_amount - fee # 1000 left as fee
    rtx.tx_out2["value"] = struct.pack("<Q", return_value)
    rtx.tx_out2["pk_script"] = bytes.fromhex("76a914%s88ac" % my_hashed_pubkey)
    rtx.tx_out2["pk_script_bytes"] = struct.pack("<B", len(rtx.tx_out2["pk_script"]))
    # =========================================
    # form raw_tx
    raw_tx_string = (
            rtx.version
            + rtx.tx_in_count
            + rtx.tx_in["txouthash"]
            + rtx.tx_in["tx_out_index"]
            + rtx.tx_in["scrip_bytes"]
            + rtx.tx_in["script"]
            + rtx.tx_in["sequence"]
            + rtx.tx_out_count
            + rtx.tx_out1["value"]
            + rtx.tx_out1["pk_script_bytes"]
            + rtx.tx_out1["pk_script"]
            + rtx.tx_out2["value"]
            + rtx.tx_out2["pk_script_bytes"]
            + rtx.tx_out2["pk_script"]
            + rtx.lock_time
            + struct.pack("<L", 1)
    )
    print("txouthash------>>", rtx.tx_in["txouthash"].hex()[::-1])
    print("script---->>>>>>", rtx.tx_in["script"].hex())
    print("message------>>>", raw_tx_string.hex())

    hashed_tx_to_sign = hashlib.sha256(hashlib.sha256(raw_tx_string).digest()).digest()
    pk_bytes = bytes.fromhex(my_private_key_hex)
    print("iii->>>>>", binascii.unhexlify(my_private_key_hex))
    print("iii->>>>>", pk_bytes)
    sk = ecdsa.SigningKey.from_string(pk_bytes, curve=ecdsa.SECP256k1)
    # vk = sk.verifying_key

    # can be used for uncompressed pubkey
    # vk_string = vk.to_string()
    # public_key_bytes = b'\04' + vk_string

    public_key_bytes_hex = sender_compressed_pub

    signature = sk.sign_digest(hashed_tx_to_sign, sigencode=ecdsa.util.sigencode_der_canonize)

    print("===============", signature.hex())

    sigscript = (

            signature
            + b'\01'
            + struct.pack("<B", len(bytes.fromhex(public_key_bytes_hex)))
            + bytes.fromhex(public_key_bytes_hex)

    )

    real_tx = (
            rtx.version
            + rtx.tx_in_count
            + rtx.tx_in["txouthash"]
            + rtx.tx_in["tx_out_index"]
            + struct.pack("<B", len(sigscript) + 1)
            + struct.pack("<B", len(signature) + 1)
            + sigscript
            + rtx.tx_in["sequence"]
            + rtx.tx_out_count
            + rtx.tx_out1["value"]
            + rtx.tx_out1["pk_script_bytes"]
            + rtx.tx_out1["pk_script"]
            + rtx.tx_out2["value"]
            + rtx.tx_out2["pk_script_bytes"]
            + rtx.tx_out2["pk_script"]
            + rtx.lock_time

    )
    print("raw_tx " + '=' * 30)
    print(real_tx.hex())


def main():
    make_raw_transaction()
    pass


if __name__ == "__main__":
    main()
