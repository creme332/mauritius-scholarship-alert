#!venv/bin/python3
from redmail import gmail
import os
from dotenv import load_dotenv, find_dotenv
import datetime

def sendEmail(emailSubject, emailBodyhtml, recipient):
    load_dotenv(find_dotenv())
    gmail.username = 'c34560814@gmail.com' 
    if(os.getenv('EMAIL_PASSCODE') is None):
        raise SystemExit("EMAIL_PASSCODE not found!")

    gmail.password  = os.getenv('EMAIL_PASSCODE')
    try:
        gmail.send(
            subject=emailSubject,
            receivers=recipient,
            text=emailBodyhtml
        )
    except Exception as e:
        raise SystemExit(e)

if __name__ == "__main__":
    emailSubject = ('{:%Y-%m-%d %H:%M:%S}'.
                    format(datetime.datetime.now()))
    recipient = 'c34560814@gmail.com'
    sendEmail(emailSubject,"this is a test",recipient)
