#!venv/bin/python3
from redmail import gmail
import os
from dotenv import load_dotenv, find_dotenv

def sendEmail(emailSubject, emailBodyhtml, recipient):
    # for local testing
    # load_dotenv(find_dotenv())
    # gmail.password  = os.getenv('EMAIL_PASSCODE')
    # print(os.getenv('EMAIL_PASSCODE'))

    gmail.username = 'c34560814@gmail.com' 
    # for github actions 
    gmail.password = os.environ['EMAIL_PASSCODE']

    gmail.send(
        subject=emailSubject,
        receivers=recipient,
        text=emailBodyhtml
    )
# emailSubject = ('{:%Y-%m-%d %H:%M:%S}'.
#                  format(datetime.datetime.now()))
# recipientList = ['c34560814@gmail.com','cosmiczorve@gmail.com']
# sendEmail(emailSubject,"tset",recipientList)
