import dateutil.parser as dparser
import pytz
from datetime import datetime
from models.communique import Communique
from emailer.emailer import Emailer
DEADLINE_GAP = 3  # numbers of days before closing date to send reminder


def must_send_reminder(communique: Communique) -> bool:
    """Checks if a reminder must be sent for a given communique.

    Args:
        communique (Communique): A Communique object.

    Returns:
        bool: True if a reminder must be sent
    """

    # if communique has no closing date, ignore
    if len(communique.closing_date.strip()) == 0:
        return False

    # extract list of user-defined communiques from scholarships.txt
    user_reminders = []
    with open('data/reminders.txt', 'r') as f:
        for scholarship in f:
            user_reminders.append(scholarship.strip())

    # if file is empty, never send a reminder.
    if len(user_reminders) == 0:
        return False

    # if user is not interested in current communique and user is
    # not interested in all scholarships, return false
    if (communique.title not in user_reminders and
            user_reminders[0] != '*'):
        return False

    # at this point user is interested with current communique

    # decide if it is the right time to send the reminder

    # Note : Timezone on ubuntu server is different from timezone in MU
    # Get current time in mauritius timezone
    MU_TIMEZONE = pytz.timezone('Indian/Mauritius')
    MU_TIME = datetime.now(MU_TIMEZONE)

    try:
        # convert closing date to a correct format and set timezone to MU
        formatted_date = dparser.parse(
            communique.closing_date, fuzzy=True, default=MU_TIME)
    except Exception:  # skip dates which cannot be parsed
        return False
    else:
        diff = (formatted_date - MU_TIME).days
        if (diff < 0):  # closing date is in the past
            return False
        if (diff == DEADLINE_GAP):
            return True
    return False


def send_reminders(all_communiques: list[Communique]) -> None:
    """Sends reminders (if any) for active communiques. An active
    communique is a communique currently displayed on the scholarship
    website.

    Args:
        all_communiques (list[Communique]): A list of all communiques on
        the scholarship website.

        NOTE: Do not pass a list of newly scraped
        communiques as deadlines for older communiques may have changed.
    """
    emailer = Emailer()
    for current_communique in all_communiques:
        if must_send_reminder(current_communique):
            emailer.send_reminder(current_communique.title)
    print(emailer.sent_count, "closing dates reminders were sent !")


if __name__ == "__main__":
    print(must_send_reminder(Communique("tets", "23 december 2023")))
