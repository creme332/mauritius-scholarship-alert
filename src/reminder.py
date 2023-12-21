from models.communique import Communique
from communique_manager import CommuniqueManager
from emailer.emailer import Emailer
from utils import clean_string
DEADLINE_GAP = 3  # numbers of days before closing date to send reminder


def must_send_reminder(communique: Communique,
                       reminder_settings: list[str]) -> bool:
    """Checks if a reminder must be sent for a given communique.

    Args:
        communique (Communique): A Communique object.

    Returns:
        bool: True if a reminder must be sent
    """

    # if communique has no closing date, ignore
    if len(clean_string(communique.closing_date)) == 0:
        return False

    # if user has not defined current communique in reminder settings,
    # ignore
    if not communique.match_reminder_settings(reminder_settings):
        return False

    # at this point user is interested with current communique.
    # decide if it is the right time to send the reminder
    try:
        if (communique.get_days_from_deadline() == DEADLINE_GAP):
            return True
    except Exception:  # skip dates which cannot be parsed
        return False


def handle_reminders(all_communiques: list[Communique]) -> None:
    """Given a list of all communiques present on website,
    this method sends reminders for communiques whose deadline
    is approaching.

    Args:
        all_communiques (list[Communique]): A list of all communiques on
        the scholarship website.

        NOTE: Do not pass a list of newly scraped
        communiques as deadlines for older communiques may have changed.
    """
    reminder_settings = CommuniqueManager().get_reminder_settings()

    # if reminder is disabled, do not send any
    if (len(reminder_settings) == 0):
        return

    emailer = Emailer()
    for current_communique in all_communiques:
        if must_send_reminder(current_communique,  reminder_settings):
            emailer.send_reminder(current_communique)
    print(emailer.sent_count, "reminders were sent !")
