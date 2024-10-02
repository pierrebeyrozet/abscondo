from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class Encrypter:
    def __init__(self, key):
        self.key = key

    def encrypt(self, payload):
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_data = pad(payload, AES.block_size)
        ciphertext = cipher.encrypt(padded_data)
        return iv + ciphertext

    def decrypt(self, payload):
        iv = payload[:AES.block_size]
        ciphertext = payload[AES.block_size:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext)
        return unpad(decrypted, AES.block_size)
