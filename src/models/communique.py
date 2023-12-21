import datetime
from communique_manager import CommuniqueManager
from utils import clean_string
import dateutil.parser as dparser
import pytz


class Communique:
    def __init__(self, title: str = "", closing_date: str = "",
                 urls: list[str] = []):
        self.title = title  # main title as displayed on website
        self.closing_date = closing_date  # as displayed on website
        self.urls = urls  # all links available for current communique

        # save time at which object was created
        self.timestamp = ('{:%Y-%m-%d %H:%M:%S}'.
                          format(datetime.datetime.now()))

    def to_dict(self):
        return vars(self)

    def to_list(self):
        return [self.title, self.closing_date, self.urls, self.timestamp]

    def match_user_interests(self, interests: list[str]) -> bool:
        """
        Checks if communique matches given user interests by checking
        if communique title contains at least 1 keyword from
        `filters.txt`.

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
        return self.title in important_communiques

    def is_last_scraped_communique(self):
        last_communique = CommuniqueManager().get_last_communique()

        # TODO: take into consideration closing date
        # if last communique undefined, return true.
        # else if communique matches the title of the last communique,
        # return true
        return ((not last_communique) or
                (clean_string(self.title)
                 == clean_string(last_communique.title)))

    def get_days_from_deadline(self) -> int:
        """
        A negative value indicates that closing date is in the past

        Raises:
            Exception: Closing date missing
            Exception: Closing date has an invalid format

        Returns:
            int: _description_
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
