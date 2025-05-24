from Crypto.Cipher import AES
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

DIR_JSON = Path(__file__).parent / 'data.json'
DIR_DUMP = Path(__file__).parent / 'dump.json'
KEY = os.getenv('KEY_AES', '')
KEY_BYTES = KEY.encode('utf-8')

def encrypt(plaintext, key):
    aes = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = aes.encrypt_and_digest(plaintext)
    return aes.nonce.hex() + tag.hex() + ciphertext.hex()

def decrypt(ciphertext, key):
    ciphertext_bytes = bytes.fromhex(ciphertext)
    nonce = ciphertext_bytes[:16]
    tag = ciphertext_bytes[16:32]
    cipher = ciphertext_bytes[32:]
    aes = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = aes.decrypt_and_verify(cipher, tag)
    return plaintext

if __name__ == '__main__':
    with open(DIR_JSON, 'rb') as file:
        data = file.read()

    with open(DIR_DUMP, 'w') as file:
        file.write(encrypt(data, KEY_BYTES))