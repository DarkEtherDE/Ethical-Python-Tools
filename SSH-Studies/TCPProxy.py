import sys
import socket
import threading

HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])
#Create a string holding ascii printable characters
#uses 3 because the join takes quotes ('') as well as character (A) for a total of 3

def hexdump(src, length = 16, show=True):
    if isinstance(src, bytes):                  #ensure string exists and decode if it exists
        src = src.decode()
    results = list()
    for i in range(0, len(src), length):
        word = str(src[i:i+length])             #Grab a piece of the string, dump it into the word variable

        printable = word.translate(HEX_FILTER)  
        #Use the built in translate function in order to substitute strings for representations of each character

        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length*3
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')
        #Creates a byte construction of the data and its conversion from byte to ascii to text

    if show:
        for line in results:
            print(line)
    
    else:
        return results

def receive_from(connection):
    buffer = b""
    connection.settimeout(5)    #data timeout to end connection every 5 seconds
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data      #sets data to buffer
    
    except Exception as e:
        pass
    return buffer               #returns data as buffer

def request_handler(buffer):
    #perform packet modifications
    return buffer

def response_handler(buffer):
    #perform packet modifications
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))                       #create connection
    success = b'Successful connect: \n'
    remote_socket.send(success)

    if receive_first:                                                       #Check for data waiting   
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)                         #Receive, dump, then continue message on to client
    if len(remote_buffer):                                                  
        print("[==>]Received %d bytes from localhost." % len(remote_buffer))
        client_socket.send(remote_buffer)
    
    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = "[<==] Recieived %d bytes from remote." % len(remote_buffer)
            print(line)
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost.")

        if not len(local_buffer) or not len(remote_buffer):                 #when text is empty, close both connections. 
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. closing connections.")
            break

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                      #create socket
    try:
        server.bind((local_host, local_port))                                       #bind to listen on local host
    except Exception as e:
        print('problem on bind: %r' % e)
    
        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)

    print("[*] Listening on %s:%d" % (local_host, local_port))
    server.listen(5)
    while True:                                                                     #main loop: new connection request is passed
        client_socket, addr = server.accept()                                       #on to proxy handler
        #print out the local connection information
        line = "> Received incoming connection from %s:%d" % (addr[0], addr[1])
        print(line)
        #start thread for remote host
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()
        #all the sending and recieving of data to both ends of the data stream

def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport]", end='')
        print("[remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 T")
        sys.exit(0)
    local_host = sys.argv[1]            #argument 1 links to local host: Per Example (127.0.0.1)
    local_port = int(sys.argv[2])       #argument 2 links to local port: Per Example (9000)
    remote_host = sys.argv[3]           #argument 3 links to remote host: Per Example 10.12.132.1
    remote_port = int(sys.argv[4])      #argument 4 links to remote port: Per Example 9000      

    receive_first = sys.argv[5]         #Get bool response from receive first

    if "True" in receive_first or "T" in receive_first:
        receive_first = True
    else:
        receive_first = False   

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == '__main__':
    main()
