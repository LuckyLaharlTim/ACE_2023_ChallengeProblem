import asyncio
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA

# class for trusted certificate authority
#  pairs users/senders with their DH exchange public key and RSA certificate key
class CertificateAuthority:

    def __init__(self):
        # initialize empty dictionaries for relevant keys
        self.dh_key_dict = {}
        self.cert_key_dict = {}

    def dh_request_handler(self, user):
        # check for and return the dh key of a message's sender
        if user in self.dh_key_dict.keys():
            return self.dh_key_dict[user]
        else:
            return "No user found"

    def cert_request_handler(self, user):
        # check for and return the RSA certificate of a message's sender
        if user in self.cert_key_dict.keys():
            return self.cert_key_dict[user]
        else:
            return "No user found"

    # add relevant <user>:<identifying key> key value pairs
    def add_user_cert(self, user, key):
        self.cert_key_dict[user] = key

    # allows for certificate revocation
    def add_user_dh_public(self, user, key):
        self.dh_key_dict[user] = key
