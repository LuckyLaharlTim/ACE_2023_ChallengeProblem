from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Random.random import randrange 
import binascii, pyDH, hmac
import rsa
import hashlib
import asyncio
from Crypto.Util.Padding import pad, unpad
from cert_authority import CertificateAuthority

## SYMMETRIC ENCRYPTION ALGORITHM ##
# aes-256 #
#- counter mode with padding
# add Padding, consider sizes
class EncryptionScheme():

    def __init__(self, user_name, cert_authority):
        self.user_name = user_name
        self.cert_authority = cert_authority
        self.__dh_secret = pyDH.DiffieHellman(14)
        self.cert_authority.add_user_dh_public(self.user_name, self.__dh_secret.gen_public_key())
        self.__cert_private_key = self.RSA_cert_gen()

    def encrypt_message(self, message, receiver):
        #Generate Initialization Vector
        IV = get_random_bytes(16)
        receiver_pub_key = self.cert_authority.dh_request_handler(receiver)
        aes_key = self.DH(receiver_pub_key, receiver)
        #Generate block cypher
        cipher = AES.new(aes_key[0:32], AES.MODE_CBC, IV)
        #Perform block cypher encryption
        ct = cipher.encrypt(pad(message, AES.block_size))
        #Convert cypher-text to hex, and merge it with the initialization vector
        ct = binascii.hexlify(cipher.iv) + binascii.hexlify(ct)
        return ct

    def decrypt_data(self, data, receiver):
        #Initialization vector is taken and converted to a usable value
        IV = binascii.unhexlify(data[0:32])
        #Ciphertext is taken and converted to a usable value
        ct = binascii.unhexlify(data[32:])
        #AES block cypher is produced
        receiver_pub_key = self.cert_authority.dh_request_handler(receiver)
        aes_key = self.DH(receiver_pub_key, receiver)
        cipher = AES.new(aes_key[0:32], AES.MODE_CBC, IV)
        #Decryption of cyphertext
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return(pt)

    ## SYMMETRIC MESSAGE AUTHENTICATION CODE ##
    # Encrypt Then MAC #
    #- HMAC, SHA-3-512

    ## ASYMMETRIC ENCRYPTION ALGORITHM ##
    # Diffie-Hellman Key Exchange #

    def DH(self, d2_pubkey, receiver):
        sharedkey = self.__dh_secret.gen_shared_key(d2_pubkey)
        return sharedkey.encode('utf8')
            
    def RSA_cert_gen(self):
        privkey, pubkey = rsa.newkeys(1028) # change back to 3072
        self.cert_authority.add_user_cert(self.user_name, pubkey)
        return privkey


    #encrpyt then mac
    def authentication_code(self, key, cipher_text):
        packet_hmac = hmac.new(key, cipher_text, hashlib.sha3_512)
        mac = packet_hmac.hexdigest()
        return mac.encode('utf8')

    def send_message(self, message, receiver):
        encoded_message = message.encode('utf8')
        pub_key = self.cert_authority.dh_request_handler(receiver)
        key = self.DH(pub_key, receiver)
        cipher_text = self.encrypt_message(encoded_message, receiver)
        mac = self.authentication_code(key, cipher_text)
        privkey = self.__cert_private_key
        signature = rsa.encrypt(cipher_text, privkey)
        print(len(cipher_text))
        print(len(mac))
        print(len(signature))
        print(signature)
        final_packet = cipher_text + mac + signature
        print(len(final_packet))
        return final_packet

    def verify_sig(self, cipher_text, sender_cert_pub_key, signature):
        decrypt_sig = rsa.decrypt(signature, sender_cert_pub_key)
        return decrypt_sig == cipher_text

    def verify_mac(self, cipher_text, sender, mac):
        pub_key = self.cert_authority.dh_request_handler(sender)
        key = self.DH(pub_key, sender)
        test_mac = self.authentication_code(key, cipher_text)
        return test_mac == mac

    def decrypt_message(self, input_message, sender):
        message_cipher = input_message[0:64]
        mac = input_message[64: 64 + 128]
        signature = input_message[64 + 128:]
        print(signature)
        sender_cert_pub_key = self.cert_authority.cert_request_handler(sender)
        if sender_cert_pub_key is None:
            print("no cert exists")
            return None
        mac_status = self.verify_mac(message_cipher, sender, mac)
        if mac_status == False:
            print("Message integrity could not be verified")
            return None
        sig_status = self.verify_sig(message_cipher, sender_cert_pub_key, signature)
        if sig_status == False:
            print("Sender verification fail")
            return None
        print("message safe")
        return self.decrypt_data(message_cipher, sender)


if __name__ == "__main__":
    cert_authority = CertificateAuthority()
    test1 = EncryptionScheme("Pat", cert_authority)
    test2 = EncryptionScheme("Tim", cert_authority)
    message = test1.send_message("Hello", test2.user_name) # can't have two people with the same user name
    print(test2.decrypt_message(message, test1.user_name))
