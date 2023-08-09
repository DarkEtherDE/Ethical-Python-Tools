from win32com import client
import os
import random
import requests
import time


username = 'DarkEtherDE'                            #Login Credentials
password = 'pass!'                         #
api_dev_key = 'dev'    #

def plain_paste(title, contents):   
    login_url = 'https://pastebin.com/api/api_login.php'                                                #API Access login
    login_data = {'api_dev_key': api_dev_key, 'api_user_name': username, 'api_user_password': password} #Data request
    r = requests.post(login_url, data = login_data)                                                     #Send a post request
    api_user_key = r.text                                                                               #Store response in api_user_key
    paste_url = 'https://pastebin.com/api/api_post.php'                                                 #Get a new paste url

    paste_data = {                                                                                      #Get Paste Data
        'api_paste_name':title,                                                                         #
        'api_paste_code':contents.decode(),                                                             #
        'api_dev_key':api_dev_key,                                                                      #
        'api_user_key':api_user_key,                                                                    #
        'api_option': 'paste',                                                                          #
        'api_paste_private':0,                                                                          #
    }
    r = requests.post(paste_url, data = paste_data)                                                     #Send paste_data
    print(r.status_code)                                                                                #Print Status
    print(r.text)                                                                                       #Print text of r

def wait_for_browser(browser):          #Return what the current state of the browser is
    while browser.ReadyState != 4 and browser.ReadyState != 'complete':
        time.sleep(.1)

def random_sleep():                     #Select a random value between 5 and 10
    time.sleep(random.randint(5,10))

def login(ie):
    full_doc = ie.Document.all
    for elem in full_doc:
        if elem.id == 'loginform-username':
            elem.setAttribute('value', username)
        elif elem.id == 'loginform-password':
            elem.setAttribute('value', password)

    random_sleep()
    if ie.Document.forms[0].id == 'w0':
        ie.document.forms[0].submit()
    wait_for_browser(ie)

def submit(ie, title, contents):
    full_doc = ie.Document.all
    for elem in full_doc:
        if elem.id == 'postform-name':
            elem.setAttribute('value', title)
        elif elem.id == 'postform-text':
            elem.setAttribute('value', contents)

    if ie.Document.forms[0].id =='w0':
        ie.document.forms[0].submit()
    random_sleep()
    wait_for_browser(ie)

def ie_paste(title, contents):
    ie = client.Dispatch('InternetExplorer.Application')
    ie.Visible = 1
    ie.Navigate('https://pastebin.com/login')
    wait_for_browser(ie)
    login(ie)
    ie.Navigate('https://pastebin.com/')
    wait_for_browser(ie)
    submit(ie, title, contents.decode())

    ie.Quit()

if __name__ == '__main__':
    ie_paste('title', 'contents')