#!venv/bin/python3
from redmail import gmail
import os
from dotenv import load_dotenv, find_dotenv
import datetime

def sendEmail(emailSubject, emailBodyhtml):
    # setup credentials
    load_dotenv(find_dotenv())
    if(os.getenv('SENDER_EMAIL_ADDRESSS') is None):
        raise SystemExit("SENDER_EMAIL_ADDRESSS not found!")
    gmail.username = os.getenv('SENDER_EMAIL_ADDRESSS')
    
    if(os.getenv('EMAIL_PASSCODE') is None):
        raise SystemExit("EMAIL_PASSCODE not found!")
    gmail.password  = os.getenv('EMAIL_PASSCODE')

    # send email to myself
    # Note : receivers can take a list of recipients
    try:
        gmail.send(
            subject=emailSubject,
            receivers=os.getenv('SENDER_EMAIL_ADDRESSS'),
            text=emailBodyhtml
        )
    except Exception as e:
        raise SystemExit(e)

if __name__ == "__main__":
    emailSubject = ('{:%Y-%m-%d %H:%M:%S}'.
                    format(datetime.datetime.now()))
    sendEmail(emailSubject,"this is a test")
