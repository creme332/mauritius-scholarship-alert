from redmail import gmail
from dotenv import load_dotenv, find_dotenv
from jinja2 import Environment, PackageLoader, select_autoescape
from models.communique import Communique
import os


class Emailer:
    def __init__(self) -> None:
        # define maximum number of emails that can be sent
        # per program execution
        self.EMAIL_LIMIT: int = 5  # ! change this value at your own risk
        self.sent_count: int = 0  # number of emails sent

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

    def _get_reminder_template(self, communique: Communique) -> str:
        template = self.env.get_template("reminder.html")

        if (len(communique.title.strip()) == 0):
            communique.title = "missing-title"

        return template.render(
            title=communique.title,
            urls=communique.urls,
            closing_date=communique.closing_date,
        )

    def send_reminder(self, communique: Communique) -> None:
        template = self._get_reminder_template(communique)
        self._send_email("Scholarship Deadline", template)

    def _get_scholarship_template(self,
                                  communique: Communique,
                                  pdf_extract: str) -> str:
        if (len(communique.title.strip()) == 0):
            communique.title = "missing-name"

        if (len(pdf_extract.strip()) == 0):
            pdf_extract = "No text found in PDF. PDF may contain an image."

        template = self.env.get_template("scholarship.html")
        return template.render(
            name=communique.title,
            urls=communique.urls,
            pdf_extract=pdf_extract,
        )

    def send_new_scholarship(self, communique: Communique,
                             pdf_extract: str) -> None:
        template = self._get_scholarship_template(
            communique, pdf_extract)
        self._send_email(communique.title, template)

    def _send_email(self, subject: str, html_body: str,
                    receivers: list[str] = []) -> None:
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
