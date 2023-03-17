import queue
import requests
import threading
import sys
from bs4 import BeautifulSoup

AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"
EXTENSIONS = ['.php', '.bak', '.orig', '.inc']
TARGET = input("Target Website: ")
THREADS = 50
WORDLIST = "C:/Users/User/Documents/HomemadeTools/SVNDigger/all.txt"



def get_words(resume=None):#feeds words, looks for a pause, if pause found, resume from list
    def extend_words(word):
        if "." in word:
            words.put(f'/{word}')#skips append on words that already have extension
        else:
            words.put(f'/{word}/')#pulls out words
            for extension in EXTENSIONS:#append extensions to words
                words.put(f'/{word}{extension}')
    
    with open(WORDLIST) as f:
        raw_words = f.read() #read words from wordlist
    found_resume = False
    words = queue.Queue()#append words to queue
    for word in raw_words.split():
        if resume is not None:
            if found_resume:
                extend_words(word)
            elif word == resume:
                found_resume = True
                print(f'Resuming wordlist from: {resume}\n')
        else:
            print(word)
            extend_words(word)
    return words
    
def dir_bruter(words):
    headers = {'User-Agent': AGENT}
    locker = threading.Lock() #implemented to allow writing from threads to file
    
    while not words.empty():
        url = f'{TARGET}{words.get()}'#append target links to target url
        try:
            r = requests.get(url, headers=headers)#collect what connection response is recieved
        except requests.exceptions.ConnectionError:#in case of a request connection error mark as invalid and clear log
            sys.stderr.write('x');sys.stderr.flush()
            continue
        if r.status_code == 200:
            print(f'\nSuccess ({r.status_code}: {url})')#print success in new line if a file path is found
            locker.acquire()
            soup = BeautifulSoup(r.text,'html.parser')
            l = soup.find("h3")
            str1 = "".join((url, ': ', str(r.status_code),'\n'))
            text = str(l)
            print(text)
            if "While the 0bit website is getting remastered" not in text:
                print("Real")
                with open('targetsfound.txt', 'a') as t:#append to created targetsfound.txt
                    t.write(str1)
                    t.close()
            else:
                print("Fake")
            locker.release()
        elif r.status_code == 404:
            sys.stderr.write('.');sys.stderr.flush()#Print . if path exists but is inaccessible and flush error
        else:
            print(f'{r.status_code} => {url}')#return what code is thrown on a particular url
            
if __name__ == '__main__':
    words = get_words()#collect words from wordlist
    print('Press return to continue.')
    sys.stdin.readline()
    try:
        for _ in range(THREADS):#spin up all threads
            t = threading.Thread(target=dir_bruter, args=(words,))#utilize threats to use bruter directory to target links through all.txt
            t.start()
    except KeyboardInterrupt:
        sys.pause