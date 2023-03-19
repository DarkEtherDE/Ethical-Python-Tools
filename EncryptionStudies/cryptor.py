from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from io import BytesIO

import base64
import zlib

#Hybrid encryption method using AES and RSA (symmetric and asymmetric)

def generate():
    new_key = RSA.generate(2048)
    private_key = new_key.exportKey()
    public_key = new_key.publickey().exportKey()
    with open('key.pri', 'wb') as f:
        f.write(private_key)
    with open('key.pub', 'wb') as f:
        f.write(public_key)
        
def get_rsa_cipher(keytype):

    with open(f'key.{keytype}') as f:
        key = f.read()
    rsakey = RSA.importKey(key)
    return (PKCS1_OAEP.new(rsakey), rsakey.size_in_bytes())
    
def encrypt(plaintext):
    compressed_text = zlib.compress(plaintext)                          #compress our text we are encrypting through zlib
    
    session_key = get_random_bytes(16)                                  #Generate a random session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX) 
    ciphertext, tag = cipher_aes.encrypt_and_digest(compressed_text)    #Perform encryption
    cipher_rsa, _ = get_rsa_cipher('pub')                               #gather public key and store in cipher_rsa
    encrypted_session_key = cipher_rsa.encrypt(session_key)             #encrypt rsa cipher
    
    msg_payload = encrypted_session_key + cipher_aes.nonce + tag + ciphertext#create the message payload
    encrypted = base64.encodebytes(msg_payload)
    return(encrypted)

def decrypt(encrypted):
    encrypted_bytes = BytesIO(base64.decodebytes(encrypted))            #Decode the byte encoding
    cipher_rsa, keysize_in_bytes = get_rsa_cipher('pri')                #Read in private key
    encrypted_session_key = encrypted_bytes.read(keysize_in_bytes)      #read in encrypted key
    nonce = encrypted_bytes.read(16)                                    #and other parameters
    tag = encrypted_bytes.read(16)                                      #
    ciphertext = encrypted_bytes.read()                                 #
    
    session_key = cipher_rsa.decrypt(encrypted_session_key)             #Decrypt the message itself
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)             
    decrypted = cipher_aes.decrypt_and_verify(ciphertext, tag)          #decrypt with key and tag
    
    plaintext = zlib.decompress(decrypted)
    return plaintext
    
if __name__ == '__main__':
    plaintext = b'hey there you'
    try:
        print(decrypt(encrypt(plaintext)))
    except FileNotFoundError:                   #If keys don't exist, generate keys and continue
        generate()
        print(decrypt(encrypt(plaintext)))