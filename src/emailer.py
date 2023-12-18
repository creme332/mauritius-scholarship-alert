from redmail import gmail
import os
from dotenv import load_dotenv, find_dotenv
import datetime


class Emailer:
    def __init__(self):
        load_dotenv(find_dotenv())

        # load email
        self.sender_email = os.getenv('SENDER_EMAIL_ADDRESS')
        if (self.sender_email is None):
            raise SystemExit("SENDER_EMAIL_ADDRESS is missing from .env file!")

        # load password
        self.password = os.getenv('EMAIL_PASSCODE')
        if (self.password is None):
            raise SystemExit("EMAIL_PASSCODE is missing from .env file!")

    def sendEmail(self, subject, body, receivers=[]):
        """Send an email to yourseld

        Args:
            emailSubject (_type_): _description_
            emailBodyhtml (_type_): _description_

        Raises:
            SystemExit: SENDER_EMAIL_ADDRESS not found
            SystemExit: EMAIL_PASSCODE not found
            SystemExit: Sending email was unsuccessful
        """
        gmail.user_name = self.sender_email
        gmail.password = self.password

        # send email to sender himself if no other recipient specified
        if (len(receivers) == 0):
            receivers = self.sender_email

        try:
            gmail.send(
                subject=subject,
                receivers=receivers,
                text=body
            )
        except Exception as e:
            raise SystemExit(e)


if __name__ == "__main__":
    emailer = Emailer()
    emailSubject = ('{:%Y-%m-%d %H:%M:%S}'.
                    format(datetime.datetime.now()))
    emailer.sendEmail(emailSubject, "this is a test")
