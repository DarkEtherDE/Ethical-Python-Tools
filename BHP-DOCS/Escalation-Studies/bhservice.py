import os
import servicemanager
import shutil
import subprocess
import sys

import win32event
import win32service
import win32serviceutil

#THIS FILE IS A DEMO FILE TO CREATE AND SETUP A TASK WITH A GHOST SERVICE ON A 
#TARGET MACHINE

SRCDIR = os.getcwd                                                  #Set source directory to where this script is run from
TGTDIR = 'C:\\Windows\\TEMP'                                        #Set target directory to TEMP

class BHServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "BlackHatService"                                  #Name
    _svc_display_name_ = "Black Hat Service"                        #Display Name
    _svc_description_ = ("Executes VBScripts at regular intervals." + " What could possibly go wrong?")

    def __init__(self, args):                                       #Initialize service, target bhservice_vbs, and set timeout of one minute as well as creating the event object
        self.vbs = os.path.join(TGTDIR, 'bhservice_task.vbs')       #Target script
        self.timeout = 1000 * 60                                    #Timeout

        win32serviceutil.ServiceFramework.__init__(self, args)      #Initialize framework
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)   #Create event

    def SvcStop(self):                                              #Set service status
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING) #Service stop status update
        win32event.SetEvent(self.hWaitStop)                         #Stop event

    def SvcDoRun(self):                                             #Start service
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)      #Service start event
        self.main()                                                 #Run main     

    def main(self):
        while True:                                                 #Set loop for every minute
            ret_code = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            if ret_code == win32event.WAIT_OBJECT_0:                #Repeat every  minute till recieve stop
                servicemanager.LogInfoMsg("Service is stopping")    
                break
            
            src = os.path.join(SRCDIR, 'bhservice_task.vbs')        #Set source
            shutil.copy(src, self.vbs)                              #copy vbs script from src
            subprocess.call("cscript.exe %s" % self.vbs, shell=False)#Execute script without shell
            os.unlink(self.vbs)                                     #Remove after running

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(BHServerSvc)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(BHServerSvc)
