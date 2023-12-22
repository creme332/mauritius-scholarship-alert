from datetime import datetime
from utils import clean_string
import dateutil.parser as dparser
import pytz


class Communique:
    def __init__(self, title: str = "", closing_date: str = "",
                 urls: list[str] = []):
        self.title = title
        self.closing_date = closing_date

        # all pdf links available for current communique on website
        self.urls = urls

        # save time at which object was created
        self.timestamp = ('{:%Y-%m-%d %H:%M:%S}'.
                          format(datetime.now()))

    def to_dict(self):
        return vars(self)

    def to_list(self):
        return [self.title, self.closing_date, self.urls, self.timestamp]

    def match_user_interests(self, interests: list[str]) -> bool:
        """
        Checks if communique matches user interest based on list of user
        interests.

        Returns:
            bool: True if condition satisfied.
        """
        # Replace U+2019 char with normal apostrophe and
        # convert to lowercase
        formatted_title = self.title.replace('’', "'").lower()

        # check if no interests were defined
        if len(interests) == 0:
            return False

        if interests[0] == "*":
            return True

        for interest in interests:
            if interest.lower() in formatted_title:
                return True
        return False

    def match_reminder_settings(self,
                                important_communiques: list[str]) -> bool:
        """
        Checks if user wants to be reminded of deadline of communique.

        Args:
            important_communiques (list[str]): A list of communique titles set
            by user so that user receives a reminder.

        Returns:
            bool: True if user wants to reminded of deadline of communique
        """
        # if no settings defined, return false
        if len(important_communiques) == 0:
            return False

        return (important_communiques[0] == "*" or
                self.title in important_communiques)

    def get_days_from_deadline(self) -> int:
        """
        Returns the number of days between today and closing date.

        Raises:
            Exception: Closing date missing
            Exception: Closing date has an invalid format

        Returns:
            int: Number of days from today to closing date. A negative value
            indicates that closing date is in the past.
        """
        # if no closing date present, return 0
        if len(clean_string(self.closing_date)) == 0:
            raise Exception("Closing date missing")

        # Note: Timezone on ubuntu server is different from timezone in MU

        # Get current time in mauritius timezone
        MU_TIMEZONE = pytz.timezone('Indian/Mauritius')
        MU_TIME = datetime.now(MU_TIMEZONE)

        # convert closing date to a correct format and set timezone to MU
        try:
            parsed_date = dparser.parse(
                self.closing_date, fuzzy=True, default=MU_TIME)
        except Exception:
            raise Exception("Closing date has an invalid format")
        else:
            return (parsed_date - MU_TIME).days
