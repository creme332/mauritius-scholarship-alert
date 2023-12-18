import dateutil.parser as dparser
import pytz
from datetime import datetime


def mustSendReminder(communiqueTitle, closingDate):
    """Check if a reminder must be sent for the communique 
    passed as parameter.

    Args:
        communiqueTitle (string): title of communique as scraped from website.
        closingDate (string): closing date of scholarship as scraped from website.

    Returns:
        Boolean: True if a reminder must be sent
    """

    # extract list of user-defined communiques from scholarships.txt
    importantScholarshipsList = []
    with open('data/scholarships.txt', 'r') as f:
        for scholarship in f:
            importantScholarshipsList.append(scholarship.strip())

    # if user did not define any important scholarships, send no reminder.
    if len(importantScholarshipsList) == 0:
        return False

    # if user is not interested in current communique and user is
    # not interested in all scholarships
    if (communiqueTitle not in importantScholarshipsList and
            importantScholarshipsList[0] != '*'):
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
        correctlyFormattedDate = dparser.parse(
            closingDate, fuzzy=True, default=MU_TIME)
    except Exception as e:  # skip dates which are impossible to understand
        return False
    else:
        diff = (correctlyFormattedDate - MU_TIME).days
        if (diff < 0):  # closing date is in the past
            return False
        if (diff == DEFAULT_GAP):
            return True
    return False


if __name__ == "__main__":
    print(mustSendReminder("super", "19 september 2022"))
