#!venv/bin/python3
from redmail import gmail
import os
from dotenv import load_dotenv, find_dotenv
import datetime

def sendEmail(emailSubject, emailBodyhtml, recipient):
    load_dotenv(find_dotenv())
    gmail.password  = os.getenv('EMAIL_PASSCODE')
    gmail.username = 'c34560814@gmail.com' 

    gmail.send(
        subject=emailSubject,
        receivers=recipient,
        text=emailBodyhtml
    )

if __name__ == "__main__":
    emailSubject = ('{:%Y-%m-%d %H:%M:%S}'.
                    format(datetime.datetime.now()))
    recipient = 'c34560814@gmail.com'
    sendEmail(emailSubject,"this is a test",recipient)
