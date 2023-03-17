import contextlib
import os
import queue
import requests
import sys
import threading
import time

FILTERED = [".jpg", ".gif", ".png", ".css"]
TARGET = "http://localhost:80/WordPress" #Target website
THREADS = 10

answers = queue.Queue()
web_paths = queue.Queue()

def run():
    mythreads = list()
    for i in range(THREADS):
        print(f'spawning thread {i}')
        t = threading.Thread(target=test_remote)
        mythreads.append(t)
        t.start()
    for thread in mythreads:
        thread.join()

def gather_paths():#Locate paths found in personal deployment folder system
    for root, _, files in os.walk('.'):
        for fname in files:
            if os.path.splitext(fname)[1] in FILTERED:
                continue
            path = os.path.join(root, fname)
            if path.startswith('.'):
                path = path[1:]
                web_paths.put(path)
                
def test_remote():
    try:
        while not web_paths.empty():
            path = web_paths.get()
            url = f'{TARGET}{path}'
            time.sleep(2) #allow threads to speed up
            urlC = url.replace('\\','/')# solution to difference in windows file paths to unix standard. Applicable in both as windows is the only instance to use \\ instead of /
            r = requests.get(urlC)
            if r.status_code == 200:#If webpage is found
                answers.put(urlC)
                sys.stdout.write('+')
            else:#if webpage is not accessible
                sys.stdout.write('x')
            sys.stdout.flush()
    except KeyboardInterrupt():
        sys.exit()
@contextlib.contextmanager
def chdir(path):
    """
    on next enter, change directory to specified path
    on exit, change directory back to original
    """
    this_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(this_dir)

if __name__ == '__main__':
    with chdir("C:/Users/User/Downloads/wordpress-6.1.1/wordpress"):
        gather_paths()
    input('Press enter to continue')#wait for response before continuing paths
    
    run()
    with open('myanswers.txt', 'w') as f:#write any located filepaths to myanswers.txt
        while not answers.empty():
            f.write(f'{answers.get()}\n')
            
    print('Done')
    
