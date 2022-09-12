#!venv/bin/python3
from redmail import gmail
import datetime
import os

def sendEmail(emailSubject, emailBodyhtml, recipient):
    gmail.username = 'c34560814@gmail.com' 
    gmail.password = os.environ.get('EMAIL_PASSCODE')

    gmail.send(
        subject=emailSubject,
        receivers=recipient,
        html=emailBodyhtml
    )

# emailSubject = ('{:%Y-%m-%d %H:%M:%S}'.
#                  format(datetime.datetime.now()))
# recipientList = ['c34560814@gmail.com','cosmiczorve@gmail.com']
# sendEmail(emailSubject,"tset",recipientList)
