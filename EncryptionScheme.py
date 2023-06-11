from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Random.random import randrange 
import binascii, pyDH, hmac
import rsa
import hashlib
import asyncio
from Crypto.Util.Padding import pad, unpad
from cert_authority import CertificateAuthority

class EncryptionScheme():

    def __init__(self, user_name, cert_authority,seq_num=0):
        self.sequence_num_dict = {}
        self.sequence_num = seq_num
        self.user_name = user_name
        self.cert_authority = cert_authority
        self.__dh_secret = pyDH.DiffieHellman(15)
        self.cert_authority.add_user_dh_public(self.user_name, self.__dh_secret.gen_public_key())
        self.__cert_private_key = self.RSA_cert_gen()

    # encrypts message using shared key of parties with padded AES-256 CBC method
    def encrypt_message(self, message, receiver):
        #Generate Initialization Vector
        IV = get_random_bytes(16)
        receiver_pub_key = self.cert_authority.dh_request_handler(receiver)
        aes_key = self.DH(receiver_pub_key)
        #Generate block cypher
        cipher = AES.new(aes_key[0:32], AES.MODE_CBC, IV)
        #Perform block cypher encryption
        ct = cipher.encrypt(pad(message, AES.block_size))
        #Convert cypher-text to hex, and merge it with the initialization vector
        ct = binascii.hexlify(cipher.iv) + binascii.hexlify(ct)
        return ct

    # decrypts message using shared key of parties with padded AES-256 CBC method
    def decrypt_data(self, data, receiver):
        #Initialization vector is taken and converted to a usable value
        IV = binascii.unhexlify(data[0:32])
        #Ciphertext is taken and converted to a usable value
        ct = binascii.unhexlify(data[32:])
        #AES block cypher is produced
        receiver_pub_key = self.cert_authority.dh_request_handler(receiver)
        aes_key = self.DH(receiver_pub_key)
        cipher = AES.new(aes_key[0:32], AES.MODE_CBC, IV)
        #Decryption of cyphertext
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return(pt)    

    # given the current object and other party's public keys
    #  computes and returns a shared key
    def DH(self, d2_pubkey):
        sharedkey = self.__dh_secret.gen_shared_key(d2_pubkey)
        return sharedkey.encode('utf8')
    
    # generates RSA public and private keys
    #  stores public in the certificate
    #  returns the private key for the object instance's reference
    def RSA_cert_gen(self):
        privkey, pubkey = rsa.newkeys(3072) # change back to 3072
        self.cert_authority.add_user_cert(self.user_name, pubkey)
        return privkey


    # encrpyt then mac; HMAC, SHA-3-512
    def authentication_code(self, key, cipher_text):
        packet_hmac = hmac.new(key, cipher_text, hashlib.sha3_512)
        mac = packet_hmac.hexdigest()
        return mac.encode('utf8')

    # gets current sequence number and increments instance's value
    def get_sequence_num(self):
        seq_str = str(self.sequence_num)
        while len(seq_str) < 5:
            seq_str = "0" + seq_str
        self.sequence_num += 1
        return seq_str

    # given message and intended recipient, crafts keys given sender and receiver
    #  knowledge and builds encryption built from...
    #  1) AES cipher_text
    #  2) HMAC using DH key
    #  3) RSA signature
    def send_message(self, message, receiver):
        message_and_seq = message + self.get_sequence_num() # addtion of fixed length seq number 
        encoded_message = message_and_seq.encode('utf8')
        pub_key = self.cert_authority.dh_request_handler(receiver) # certificate public key
        key = self.DH(pub_key)
        cipher_text = self.encrypt_message(encoded_message, receiver) # AES encryption
        mac = self.authentication_code(key, cipher_text) 
        privkey = self.__cert_private_key
        signature = rsa.encrypt(cipher_text, privkey)
        final_packet = (cipher_text, mac, signature) # final message is concatination of three pieces
        return final_packet

    # check that ciphertext contains the proper signature and offset bytes
    #  signature checked through rsa decryption
    def verify_sig(self, cipher_text, sender_cert_pub_key, signature):
        decrypt_sig = rsa.decrypt(signature, sender_cert_pub_key)
        return decrypt_sig == cipher_text

    # check if mac made using shared DH key matches received mac
    def verify_mac(self, cipher_text, sender, mac):
        pub_key = self.cert_authority.dh_request_handler(sender)
        key = self.DH(pub_key)
        test_mac = self.authentication_code(key, cipher_text)
        return test_mac == mac

    # decrypt message checking
    #  1) certificate signature 
    #  2) MAC 
    #  3) sender's public key
    #  4) sequence number (to prevent replays)
    def decrypt_message(self, input_message, sender):
        message_cipher = input_message[0]
        mac = input_message[1]
        signature = input_message[2]
        sender_cert_pub_key = self.cert_authority.cert_request_handler(sender)
        if sender_cert_pub_key is None: # looks for certificate public key
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
        message_and_seq = self.decrypt_data(message_cipher, sender)
        if self.check_seq(sender, message_and_seq[-5:]) == False:
            print("replay attack detected")
            return None
        print("message authenticated")
        return message_and_seq[:-5]
    
    # check that message is a replay by sequence number
    #  add current sequence num if msg is safe
    def check_seq(self, sender, seq_num):
        int_version = int(seq_num)
        if sender not in self.sequence_num_dict.keys():
            self.sequence_num_dict[sender] = {int_version} #maps sender to set of numbers
        else:
            if int_version in self.sequence_num_dict[sender]:
                return False
            self.sequence_num_dict[sender].add(int_version)
        return True


# input accepted users in the certificate authority,
#  encrypt messages from test1 and decrypt with intended recipient.
if __name__ == "__main__":
    # initialize cert_authority and messagers' certificates for inclusion therein
    cert_authority = CertificateAuthority()
    test1 = EncryptionScheme("Pat", cert_authority)
    test2 = EncryptionScheme("Sam", cert_authority)
    test3 = EncryptionScheme("Tim", cert_authority)

    # handle sending and verifying/returning messages
    message = test1.send_message("really long message test", test2.user_name) # can't have two people with the same user name
    print(test2.decrypt_message(message, test1.user_name),end="\n")
    mess2 = test1.send_message("take 2", test2.user_name)
    print(test2.decrypt_message(mess2, test1.user_name),end="\n")
    m3 = test1.send_message("len test", test2.user_name)
    print(test2.decrypt_message(m3, test1.user_name),end="\n")

