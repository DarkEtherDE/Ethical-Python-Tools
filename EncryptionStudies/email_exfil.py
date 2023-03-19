import smtplib
import time
import win32com.client

smtp_server = 'smtp.gamil.com'
smtp_port = 25
smtp_acct = 'example@randommail.com'
smtp_passwd = None
tgt_acct = ['private@arndomaladn.ws']

def plain_email(subject, contents):
    message = f'Subject: {subject}\nFrom {smtp_acct}\n'
    message += f'To: {tgt_acct}\n\n{contents.encode()}'
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_acct, smtp_passwd)
#server.set_debuglevel(1)
    server.sendmail(smtp_acct, tgt_acct, message)
    time.sleep(1)
    server.quit()
    
def outlook(subject, contents):
    outlook = win32com.client.Dispatch("Outlook.Application")
    message = outlook.CreateItem(0)
    message.DeleteAfterSubmit = True
    message.Subject = subject
    message.Body = contents.decode()
    message.To = tgt_acct[0]
    message.Send()
    
if __name__ == '__main__':
    plain_email('test2 message', 'attack at dawn')
    