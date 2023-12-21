from src.emailer.emailer import Emailer
from src.models.communique import Communique

REMINDER_PATH = "tests/data/emails/reminders"

NEW_SCHOLARSHIP_PATH = "tests/data/emails/scholarships"


class TestEmailer:
    def test_reminder_template_1(self):
        communique = Communique("Scholarship for vulnerable children",
                                "18 December 2023",
                                ["a.com", "b.com", "c.com"])
        template = Emailer()._get_reminder_template(
            communique)
        print()
        print(template)
        with open(f"{REMINDER_PATH}/1.html", "r") as f:
            expected_result = f.read()
        assert template == expected_result

    def test_reminder_template_2(self):
        communique = Communique(" ",
                                "18 December 2023", ["a.com"])
        template = Emailer()._get_reminder_template(
            communique)
        print()
        print(template)
        with open(f"{REMINDER_PATH}/2.html", "r") as f:
            expected_result = f.read()
        assert template == expected_result

    def test_scholarship_template_1(self):
        communique = Communique("Scholarship for X",
                                "18 December 2023", ["a.com"])
        pdf_extract = "This is a test PDF"
        template = Emailer()._get_scholarship_template(
            communique, pdf_extract)
        print()
        print(template)
        with open(f"{NEW_SCHOLARSHIP_PATH}/1.html", "r") as f:
            expected_result = f.read()
        assert template == expected_result
