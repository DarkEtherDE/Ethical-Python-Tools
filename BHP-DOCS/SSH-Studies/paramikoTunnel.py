import paramiko

def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Add a key system! in this case, removing key requirement
    print("Add a key system!")
    client.connect(ip, port = port, username = user, password = passwd, banner_timeout=200)     
    if paramiko.AuthenticationException:
        print("Authentication Error!")
    else:

        #If connection is made, produce command. In the case of output, produce output
        _, stdout, stderr = client.exec_command(cmd)
        output = stdout.readlines() + stderr.readlines()
        if output:
            print('<---Output--->\n')
            for line in output:
                print(line.strip())
        
if __name__ == '__main__':
    import getpass
    #user = getpass.getuser()
    user = input('Username: ')
    password = getpass.getpass()

    ip = input('Enter server IP: ') or '127.0.0.1'
    port = input('Enter port or <CR>: ') or 5555
    cmd = input('Enter command or <CR>: ') or 'id'
    ssh_command(ip, port, user, password, cmd)