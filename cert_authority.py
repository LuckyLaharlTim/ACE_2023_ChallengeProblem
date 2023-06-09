import asyncio
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA

class CertificateAuthority:

    def __init__(self):
        self.dh_key_dict = {}
        self.cert_key_dict = {}

    def dh_request_handler(self, user):
        if user in self.dh_key_dict.keys():
            return self.dh_key_dict[user]
        else:
            return "No user found"

    def cert_request_handler(self, user):
        if user in self.cert_key_dict.keys():
            return self.cert_key_dict[user]
        else:
            return "No user found"

    def add_user_cert(self, user, key):
        self.cert_key_dict[user] = key

    # allows for certificate revocation
    def add_user_dh_public(self, user, key):
        self.dh_key_dict[user] = key
