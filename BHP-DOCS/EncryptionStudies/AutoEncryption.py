from Cryptodome.Cipher import AES

key = b'Sixteen byte key'
iv = b'initialization v'

ECBcipher = AES.new(key, AES.MODE_ECB)                          #Creation of an AES_ECB cipher 

CBCcipher = AES.new(key, AES.MODE_CBC, iv)                      #Creation of an AES_CBC cipher

with open("screenshot.bmp","rb") as f:                          #convert screenshot.bmp into a binary value
    plaintext = f.read()
    
excess = len(plaintext)%16                                      #returns remainder of equation plaintext/16       

plaintext_trimmed = plaintext[64:-excess]                       #Remove excess of modulus 16 from plaintext, as well as 64 character identity value of image

ciphertext = ECBcipher.encrypt(plaintext_trimmed)               #Perform encryption utilizing ECB cipher

ciphertext = plaintext[0:64] + ciphertext + plaintext[-excess:] #Amends the first 64 and characters removed from the end of the plaintext in order to put together the encrypted string.

with open("test_ecb.bmp","wb") as f:                            #Outputting your ECB cipher
    f.write(ciphertext)

ciphertext = plaintext[64:-excess]

decryptedText = ECBcipher.decrypt(ciphertext)

decryptedText = plaintext[0:64] + ciphertext + plaintext[-excess:]

with open("decrypted_test_ebc.bmp", "wb") as f:
    f.write(decryptedText)

ciphertext = CBCcipher.encrypt(plaintext_trimmed)

ciphertext = plaintext[0:64] + ciphertext + plaintext[-excess:]

with open("test_cbc.bmp", "wb") as f:
    f.write(ciphertext)