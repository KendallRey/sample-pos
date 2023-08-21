from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import base64

class AES_Cipher:
    def __init__(self, key : str, iv : str):
        self.iv = iv
        self.key = key

    def encrypt(self, data):
            data= pad(data.encode(),16)
            cipher = AES.new(self.key.encode('utf-8'),AES.MODE_CBC, self.iv)
            return base64.b64encode(cipher.encrypt(data))

    def decrypt(self, enc):
            enc = base64.b64decode(enc)
            cipher = AES.new(self.key.encode('utf-8'), AES.MODE_CBC, self.iv)
            return unpad(cipher.decrypt(enc),16)