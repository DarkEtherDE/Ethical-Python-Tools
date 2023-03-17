import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

class NetCat:
    #create socket object
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        #define the socket
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print('Link Successful: ')
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    


    def run(self):
        if self.args.listen:
            self.listen()
            print('listening in run')
        else:
            self.send()
            print('sent')

    def send(self):
        self.socket.connect((self.args.target, self.args.port)) #connection
        if self.buffer:
            self.socket.send(self.buffer)
        try:                
            while True:
                recv_len=1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len<4096:
                        break       #end data then end loop
                if response:

                    buffer = input(response)
                    buffer += '\n'
                    self.socket.send(buffer.encode())  #print respone, get input, send input
        except KeyboardInterrupt:           #ctrl-c ends program
            print('User terminated')
            self.socket.close()
            sys.exit()
    def listen(self):
        self.socket.bind((self.args.target, self.args.port))    #listen method binds to the target and port
        self.socket.listen(5)
        while True:                                             #listen in a loop
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target = self.handle, args = (client_socket,))                #pass socket to handle method
            client_thread.start()
    def handle(self, client_socket):  
        message = f''              
        if self.args.execute:                       #execute task corresponding to line argument recieved
            output = execute(self.args.execute)
            print('execution going through in handle')
            client_socket.send(output.encode())
        elif self.args.upload:                      #command passed to execute method and sends output back
            file_buffer = b''   
            while True:
                print('Upload:')
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
                    
                with open(self.args.upload, 'wb') as f:
                    f.write(file_buffer)
                message = f'Saved file {self.args.upload}'
                client_socket.send(message.encode())
        elif self.args.command:                     #set up a loop for content till no more 
            cmd_buffer = b''                        #is sent, then write content gathered
            while True:                             # to file
                try:
                    client_socket.send(b'<BHP: #>')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()


def execute(cmd):
        cmd = cmd.strip()
    
        if not cmd:
            print('break')
            return
        output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
        return output.decode()


if __name__ == '__main__':
    parser = argparse.ArgumentParser( 
    description='BHP Net Tool',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent('''Example: 
    netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
    netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
    netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command
    echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
    netcat.py -t 192.168.1.108 -p 5555 # connect to server
    '''))
    parser.add_argument('-c', '--command', action='store_true', help='command shell') 
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
    if args.listen: 
        buffer = ''
    else:
        buffer = sys.stdin.read()
    nc = NetCat(args, buffer.encode())
    nc.run()
    