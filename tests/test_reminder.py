from src.reminder import must_send_reminder, DEADLINE_GAP
from src.models.communique import Communique
from datetime import timedelta, date


class TestReminder:
    def test_missing_closing_date(self):
        assert not must_send_reminder(Communique("title", ""), [])
        assert not must_send_reminder(Communique("title", "  "), [])
        assert not must_send_reminder(Communique("title", ""), ["*"])

    def test_star_wildcard(self):
        # define a valid closing date that will trigger reminder if
        # all other conditions are met
        valid_closing_date = (
            date.today() + timedelta(days=DEADLINE_GAP)).isoformat()

        # when * wildcard is specified as first element of array,
        # user must be reminded of the approaching deadline of all communiques
        assert must_send_reminder(Communique(
            "communique 1", valid_closing_date), ["*"])
        assert must_send_reminder(Communique(
            "communique 2", valid_closing_date), ["*"])
        assert must_send_reminder(Communique(
            "communique 2", valid_closing_date), ["*", "communique 3"])
        assert must_send_reminder(Communique(
            "communique 2", valid_closing_date), ["*", "communique 3"])

        # wildcard * must be first element of array to work

        # wilcard serves no purpose in the following examples
        assert not must_send_reminder(Communique(
            "communique 3", valid_closing_date), ["communique 2", "*"])
        assert must_send_reminder(Communique(
            "communique 3", valid_closing_date), ["communique 2", "*",
                                                  "communique 3"])
