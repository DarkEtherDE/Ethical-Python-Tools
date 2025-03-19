import binascii
from collections import Counter
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad;
from datetime import datetime
from twofish import Twofish

text = b'Tinder Data Breach: 70k user pictures released from an expected 16k usersWhat happened?: It is suspected that a scraping tool was used in order to gather usernames and photos of users. Some also say that perhaps the data could be used to train facial recognition, this came paired with appearances of potential data release to marketing and ad companies without consent from users.Data stolen: Usernames and IDs as well as photos and potentially personal information provided on the users accounts. When?: Approximately January 16th is when this issue came to light, but given the suspected use of reverse api utilization it could be have been going on for months 70000 photos of female users found online it can be implied that since this hack only targeted womens tinder accounts, that their pictures and data will be used for catfishing Tinder says that they prohibit the use if scraping tools, and hackers found a way around this by reverse engineering API capabilities and collecting data through that'
key = b'Sixteen byte key' 
iv = b'initialization v'
print("Hex Distribution:")
print('')
hexText = binascii.hexlify(bytearray(text)).decode('ascii')
print(hexText)
print('')
print('')
textBin_trimmed = b''
ciphertext = b''
blockSize = 16
cipherAESCBC = AES.new(key, AES.MODE_CBC, iv)                                                   #Defines our keys
cipherTwofish = Twofish(str.encode('secret'))                                                   #||||||||||||||||

#AES CIPHER START ||||||||||||||||||||||||||
start_time = datetime.now()                                                                 #get the exact time to the millisecond    
print(start_time)
paddedText = pad(text, blockSize)                                                           #append to ensure text has a value that is a perfect modulus of blockSize
z = int(len(paddedText)/blockSize)                                                          #Finds how many intervals of trimmedText to encrypt
for j in range(z):
    ciphertext += cipherAESCBC.encrypt(paddedText[j*blockSize:(j+1)*blockSize])             #Run the encryption on paddedText in sets of blockSize
ciphertext = binascii.hexlify(bytearray(ciphertext)).decode('ascii')                        #converts from bytearray to hex
print("AES Encryption")                                                                     #Label for the encryption
print('')
print('')
print(ciphertext)
print('')   
print("Time Difference: ")
td = datetime.now() - start_time                                                            #find the difference between the start and current time of the function
print("Difference: ", td.microseconds)                                                      #print the value above in microseconds

#TwoFish CIPHER START ||||||||||||||||||||||||||
start_time = datetime.now()                                                                 #get the exact time to the millisecond    
print(start_time)
paddedText = pad(text, blockSize)                                                           #append to ensure text has a value that is a perfect modulus of blockSize
z = int(len(paddedText)/blockSize)                                                          #Finds how many intervals of trimmedText to encrypt
for j in range(z):
    ciphertext += binascii.hexlify(cipherTwofish.encrypt(paddedText[j*blockSize:(j+1)*blockSize])).decode('ascii')#Run the encryption on paddedText in sets of blockSize
print("TwoFish Encryption")                                                                 #Label for the encryption
print('')
print(ciphertext)
print("Time Difference: ")
td = datetime.now() - start_time                                                            #find the difference between the start and current time of the function
print("Difference: ", td.microseconds)                                                      #print the value above in microseconds
