from scapy.all import TCP, rdpcap
import collections
import os
import re
import sys
import zlib


if os.name == 'nt':
    print("Operating System:", os.name)
    OUTDIR = os.getcwd()    #write the files to the directory in which the file is run
    if os.path.exists(OUTDIR) is False:
        os.makedirs(OUTDIR)
    PCAPS = 'C:/Users/User/Pictures/Test'
    
else:
    print("Operating System: ", os.name)
    OUTDIR = os.getcwd()    #write the files to the directory in which the file is run
    if os.path.exists(OUTDIR) is False:
        os.makedirs(OUTDIR)
    PCAPS = '/home/kali/Downloads'

    

Response = collections.namedtuple('Response', ['header', 'payload'])#define the packet header and payload

def get_header(payload):#helping code to identify header and packet
    try:
        header_raw = payload[:payload.index(b'\r\n\r\n')+2]#locate new line pairs to find headers
    except ValueError:
        sys.stdout.write('-Error\n')
        sys.stdout.flush()  #print the - then flush error in try catch.
        return None #Return null (-) on a valueerror
    
    header = dict(re.findall(r'(?P<name>.*?): (?P<value>.*?)\r\n', header_raw.decode()))#Spliting data on the key before colon and value after, no content type(key) returns none
    if 'Content-Type' not in header:
        print('NULL')
        return None
    return header
    
def extract_content(Response, content_name='image'):
    content, content_type = None, None
    if content_name in Response.header['Content-Type']: #check what content type
        content_type = Response.header['Content-Type'].split('/')[1] #create variable declaring content type specified
        content = Response.payload[Response.payload.index(b'\r\n\r\n')+4:]#content variable
        
        if 'Content-Encoding' in Response.header:#Check for encoding and use zlib to decode if possible
            if Response.header['Content-Encoding']== "gzip":
                content = zlib.decompress(Response.payload, zlib.MAX_WBITS | 32)
            elif Response.header['Content-Encoding'] == "deflate":
                content = zlib.decompress(Response.payload)
                
    return content, content_type #return content type and contents
        
class Recapper:
    def __init__(self, fname):#Scapy feature which can seperate tcp sessions
        pcap = rdpcap(fname)
        self.sessions = pcap.sessions()#store the session into a dictionary
        self.responses = list()#create an empty list 
        
    def get_responses(self):
        for session in self.sessions:
            payload = b''
            for packet in self.sessions[session]:#Iterate through dictionary and packets
                try:
                    
                    if packet[TCP].dport == 80 or packet[TCP].sport == 80:#filter traffic through port 443
                        print("port:80")
                        payload += bytes(packet[TCP].payload)
                    else: 
                        print(packet[TCP].sport, "->" , packet[TCP].dport)
                except IndexError:
                    sys.stdout.write('x \n')#print x if error then continue
                    sys.stdout.flush()
            
            if payload:
                header = get_header(payload) #Pass http header parsing get header
                if header is None:
                    continue
                self.responses.append(Response(header=header, payload=payload))#Append responses to response list
                
    def writer(self, content_name):
        for i, response in enumerate(self.responses):#iterate responses
            content, content_type = extract_content(response, content_name)#extraction
            if content and content_type:
                fname = os.path.join(OUTDIR, f'ex_{i}.{content_type}')
                print(f'writing {fname}')
                with open(fname, 'wb') as f:
                    f.write(content)#write to file
    
if __name__ == '__main__':
    pfile = os.path.join(PCAPS, 'pcap.pcap')
    if os.path.exists(OUTDIR) is False:
            os.makedirs(OUTDIR)
            print(OUTDIR)
    try: 
        recapper = Recapper(pfile)
        
    except FileNotFoundError:
        print("ERROR: Ensure you have created the proper file paths or modified the path for your pcap file: ", PCAPS)
        exit()
    recapper.get_responses()
    recapper.writer('image')