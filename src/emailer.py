from redmail import gmail
from dotenv import load_dotenv, find_dotenv
from jinja2 import Environment, PackageLoader, select_autoescape
import os


class Emailer:
    def __init__(self):
        # define maximum number of emails that can be sent
        # per program execution
        self.EMAIL_LIMIT = 5  # ! change this value at your own risk
        self.sent_count = 0  # number of emails sent

        load_dotenv(find_dotenv())

        # load email
        self.sender_email = os.getenv('SENDER_EMAIL_ADDRESS')
        if (self.sender_email is None):
            raise SystemExit("SENDER_EMAIL_ADDRESS is missing from .env file!")

        # load password
        self.password = os.getenv('EMAIL_PASSCODE')
        if (self.password is None):
            raise SystemExit("EMAIL_PASSCODE is missing from .env file!")

        gmail.username = self.sender_email
        gmail.password = self.password

        # setup jinja for email templates
        self.env = Environment(
            loader=PackageLoader("emailer"),
            autoescape=select_autoescape()
        )

    def send_reminder(self, communique_name):
        template = self.env.get_template("reminder.html")

        if (len(communique_name.strip()) == 0):
            communique_name = "missing-name"

        html_body = template.render(
            communique_name=communique_name,
        )

        self.send_email("Scholarship Deadline", html_body)

    def send_new_scholarship(self, communique_name, communique_text):
        if (len(communique_name.strip()) == 0):
            communique_name = "missing-name"

        if (len(communique_text.strip()) == 0):
            communique_text = "No text found in PDF. PDF may contain an image."

        template = self.env.get_template("scholarship.html")
        html_body = template.render(
            communique_name=communique_name,
            communique_text=communique_text,
        )
        self.send_email(communique_name, html_body)

    def send_email(self, subject, html_body, receivers=[]):
        if (self.sent_count >= self.EMAIL_LIMIT):
            raise SystemExit("Email Limit Exceeded")

        # send email to sender himself if no other recipient specified
        if (len(receivers) == 0):
            receivers = self.sender_email

        try:
            gmail.send(
                subject=subject,
                receivers=receivers,
                html=html_body,
            )
        except Exception as e:
            raise SystemExit(e)
        self.sent_count = self.sent_count + 1


if __name__ == "__main__":
    emailer = Emailer()
    emailer.send_reminder("Test Scholarship")
    emailer.send_new_scholarship("Test Communique", "")
