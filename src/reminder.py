import dateutil.parser as dparser
import pytz
from datetime import datetime


def must_send_reminder(communique: str, closingDate: str) -> bool:
    """Checks if a reminder must be sent for a given communique.

    Args:
        communique (str): title of communique as scraped from website.
        closingDate (str): closing date of scholarship as scraped from
        website.

    Returns:
        bool: True if a reminder must be sent
    """

    # extract list of user-defined communiques from scholarships.txt
    important_scholarships = []
    with open('data/reminders.txt', 'r') as f:
        for scholarship in f:
            important_scholarships.append(scholarship.strip())

    # if user did not define any important scholarships, send no reminder.
    if len(important_scholarships) == 0:
        return False

    # if user is not interested in current communique and user is
    # not interested in all scholarships, return false
    if (communique not in important_scholarships and
            important_scholarships[0] != '*'):
        return False

    # at this point user is interested with at least 1 scholarship

    # decide if it is the right time to send the reminder
    DEFAULT_GAP = 3  # numbers of days before closing date to send reminder

    # Note : Timezone on ubuntu server is different from timezone in MU
    # Get current time in mauritius timezone
    MU_TIMEZONE = pytz.timezone('Indian/Mauritius')
    MU_TIME = datetime.now(MU_TIMEZONE)

    try:
        # convert closing date to a correct format and set timezone to MU
        formatted_date = dparser.parse(
            closingDate, fuzzy=True, default=MU_TIME)
    except Exception:  # skip dates which are impossible to understand
        return False
    else:
        diff = (formatted_date - MU_TIME).days
        if (diff < 0):  # closing date is in the past
            return False
        if (diff == DEFAULT_GAP):
            return True
    return False


if __name__ == "__main__":
    print(must_send_reminder("super", "19 september 2022"))
