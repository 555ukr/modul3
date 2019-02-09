#
# res = "a4cfc87d939bd16caeaa991b2e2a3dcf915ec6d7b17b34c62fe3d3a7d14ee2fc"
#
#
# from hashlib import sha256
# import binascii
#
# val = "01000000019c3b7b71587f3496f1f05c0bff014e1c32817be800c3ca9604bae779ab4e8458010000006b483045022100aaaca4a845f95cb69767df0a764c9351c14dbde8c07ee3132820bd1efede368a0220300b0d34f6908da126c251b52b98920eee1a1bae18b745b2187274303261c755012103387a90c1051d0fb0c68e9a313e34e27b085e445fd371420d4be08a8974d500b0ffffffff0250c30000000000001976a914c13e315661793e54a8f667d57213de804246801588ace0570e00000000001976a914ab7f2bf00cbf8cec7ba83b480be5bad69ddc40d388ac00000000"
# rt = sha256(sha256(binascii.unhexlify(val)).digest()).digest()[::-1]
# print(rt.hex())
# print(res)
# import time
#
# r = hex(int(time.mktime(time.strptime('2017-01-12 13:01:25', '%Y-%m-%d %H:%M:%S'))) - time.timezone)
#
# print(type(r))
