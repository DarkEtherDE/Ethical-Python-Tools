import os
import sys
import win32api
import win32con
import win32security
import wmi

def get_process_privilege(pid):
    try:
        hproc = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)            #Use PID to obtain a handle on the target process
        htok = win32security.OpenProcessToken(hproc, win32con.TOKEN_QUERY)                      #Look at the token data
        privs = win32security.GetTokenInformation(htok, win32security.TokenPrivileges)          #Request token info for the Process
        privileges = ''
        for priv_id, flags in privs:
            if flags == (win32security.SE_PRIVILEGE_ENABLED | win32security.SE_PRIVILEGE_ENABLED_BY_DEFAULT):#Return tuples where the first is privilege and second is is it enabled
                privileges += f'{win32security.LookupPrivilegeName(None, priv_id)}|'            #Lookup human readable name of the privilege
    except Exception as e:
        print('Exception: {}'.format(e))
        privileges = 'N/A'

    return privileges
def log_to_file(message):
    with open('process_monitor_log.csv','a') as fd:
        fd.write(f'{message}\r\n')

def monitor():
    head = 'CommandLine, Time, Executable, Parent PID, PID, User, Privileges'
    log_to_file(head)
    c = wmi.WMI()                                           #Create wmi class
    process_watcher = c.Win32_Process.watch_for('creation') #Watch for process creation
    while True:
        try:
            new_process = process_watcher()                 #Prevents until process_water returns a new event
            cmdline = new_process.commandLine
            create_date = new_process.CreationDate
            executable = new_process.ExecutablePath
            parent_pid = new_process.ParentProcessId
            pid = new_process.ProcessId
            proc_owner = new_process.GetOwner()             #Call getOwner to return owner

            privileges = get_process_privilege(pid)         #Store all data in process_log_message
            process_log_message = (f'COMMANDLINE: {cmdline}\nCREATED: {create_date}\nEXECUTABLE: {executable}\n' f'Parent PID: {parent_pid}\nPID: {pid}\nOWNER: {proc_owner}\n{privileges}\n')
            print(process_log_message)
            log_to_file(process_log_message)                #Store message in a file called process_monitor_log.csv
        except Exception as e:
            print('ERROR: {}'.format(e))
            pass

if __name__ == '__main__':
    monitor()