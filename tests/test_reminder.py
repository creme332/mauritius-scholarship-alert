from src.reminder import must_remind_user_now, DEADLINE_GAP
from src.models.communique import Communique
from datetime import timedelta, date


class TestReminder:
    def test_missing_closing_date(self):
        assert not must_remind_user_now(Communique("title", ""), ["title"])
        assert not must_remind_user_now(Communique("title", "  "), ["title"])
        assert not must_remind_user_now(Communique("title", ""), ["*"])

    def test_closing_date_other_than_now(self):
        # set closing date 5 days after today
        days_after_deadline = DEADLINE_GAP + 5
        future_closing_date = (
            date.today() + timedelta(days=days_after_deadline)).isoformat()
        assert not must_remind_user_now(Communique(
            "title", future_closing_date), ["title"])

        # set closing date 5 days before deadline
        days_after_deadline = DEADLINE_GAP - 5
        past_closing_date = (
            date.today() + timedelta(days=days_after_deadline)).isoformat()
        assert not must_remind_user_now(Communique(
            "title", past_closing_date), ["title"])

        # set closing date to today
        today = date.today().isoformat()
        assert not must_remind_user_now(Communique(
            "title", today), ["title"])

    def test_star_wildcard(self):
        # define a valid closing date that will trigger reminder if
        # all other conditions are met
        valid_closing_date = (
            date.today() + timedelta(days=DEADLINE_GAP)).isoformat()
        valid_communique = Communique("communique 1", valid_closing_date)

        # when * wildcard is specified as first element of array,
        # user must be reminded of the approaching deadline of all communiques
        assert must_remind_user_now(valid_communique, ["*"])
        assert must_remind_user_now(Communique(
            "communique 2", valid_closing_date), ["*"])
        assert must_remind_user_now(Communique(
            "communique 2", valid_closing_date), ["*", "communique 3"])
        assert must_remind_user_now(Communique(
            "communique 2", valid_closing_date), ["*", "communique 3"])

        # wildcard * must be first element of array to work
        assert not must_remind_user_now(Communique(
            "communique 3", valid_closing_date), ["communique 2", "*"])
        assert must_remind_user_now(Communique(
            "communique 3", valid_closing_date), ["communique 2", "*",
                                                  "communique 3"])
