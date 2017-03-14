import base64, hashlib

from Crypto import Random
from Crypto.Cipher import AES


key = 'D52kq3wTykHDhfz32PU5KzWQ41EOQ436'

size = 256
BS = size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-s[-1]]


class AESCipher:

    def __init__( self, key ):
        self.key = hashlib.sha256(key.encode('utf-8')).digest()

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[size:] ))


cipher = AESCipher(key)
encrypted = cipher.encrypt('My secret message')
decrypted = cipher.decrypt(encrypted)
print(encrypted)
print(decrypted)