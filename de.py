import base58


addr = 'mz4BUifRKs7xgpG6sqAaZxBBY9ABJWYrLj'
recipient_hashed_pubkey = base58.b58decode_check(addr)[1:].hex()
lock_scrip_pr = bytes.fromhex("76a914%s88ac" % recipient_hashed_pubkey)
print(lock_scrip_pr.hex())
