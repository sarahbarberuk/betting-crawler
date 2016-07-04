'''
Created on 1 Jul 2016

@author: Sarah
'''

# smtplib module send mail

import smtplib

def send():
    TO = 'oneofthebarbers@gmail.com'
    SUBJECT = 'TEST MAIL'
    TEXT = 'Here is a 2nd message from python.'
    
    # Gmail Sign In
    gmail_sender = 'sarahbarberuk@gmail.com'
    gmail_passwd = 'H05t!leSch!zm'
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)
    
    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])
    
    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print ('email sent')
    except:
        print ('error sending mail')
    
    server.quit()
    print("finished")
    return

