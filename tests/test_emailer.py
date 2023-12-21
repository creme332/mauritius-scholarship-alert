from src.emailer.emailer import Emailer
from src.models.communique import Communique

REMINDER_PATH = "tests/data/emails/reminders"

NEW_SCHOLARSHIP_PATH = "tests/data/emails/scholarships"


class TestEmailer:
    def test_reminder_template_1(self):
        x = Communique("Scholarship for vulnerable children",
                       "18 December 2023", ["a.com", "b.com", "c.com"])
        template = Emailer()._get_reminder_template(
            x)
        with open(f"{REMINDER_PATH}/1.html", "r") as f:
            expected_result = f.read()
        assert template == expected_result

    def test_reminder_template_2(self):
        x = Communique(" ",
                       "18 December 2023", ["a.com"])
        template = Emailer()._get_reminder_template(
            x)
        print()
        print(template)
        with open(f"{REMINDER_PATH}/2.html", "r") as f:
            expected_result = f.read()
        assert template == expected_result
