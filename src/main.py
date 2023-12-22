import asyncio
from communique_manager import CommuniqueManager
from utils import extract_text
from emailer.emailer import Emailer
from reminder import handle_reminders
from scraper.scraper import get_all_communiques
from scraper.request_helper import request_all
from feed import Feed


def main() -> None:
    """
    Driver function for program.
    """
    MANAGER = CommuniqueManager()

    # fetch all communiques from website
    print("Fetching all communiques...")
    all_communiques = get_all_communiques()
    print(f"Done. {len(all_communiques)} communiques found:")
    print("\n".join([c.title for c in all_communiques[:5]]))
    print("...")

    # send reminders if any
    print("Checking for reminders...")
    reminders_count = handle_reminders(all_communiques)
    print(f"Done. {reminders_count} reminders sent.")

    # remove communiques which were already scraped before
    # to get only new communiques
    new_communiques = MANAGER.get_new_communiques(all_communiques)

    print(f"{len(new_communiques)} new communiques found.")

    # if no new communiques found, exit
    if (len(new_communiques) == 0):
        return

    print("Processing PDF of each communique...")

    # each communique has at least 1 pdf
    # extract first pdf url for each communiques
    pdf_urls = [c.urls[0] for c in new_communiques]

    assert (len(pdf_urls) == len(new_communiques))

    # request pdfs
    pdf_responses = asyncio.run(request_all(pdf_urls))

    # get the pdf text from each valid response
    pdfs_text = [extract_text(r)
                 for r in pdf_responses if r.status_code == 200]

    assert (len(pdf_urls) == len(pdfs_text))

    print(f"Done. {len(pdfs_text)} PDFs extracted.")

    # get user interests
    user_interests = MANAGER.get_user_interests()

    # For send emails
    print("Sending email...")
    emailer = Emailer()
    for i in range(0, min(emailer.EMAIL_LIMIT, len(new_communiques))):
        if new_communiques[i].match_user_interests(user_interests):
            emailer.send_new_scholarship(new_communiques[i], pdfs_text[i])

    print(f"Done. {emailer.sent_count} scholarship emails were sent!")

    # update last scraped communique
    MANAGER.save(new_communiques[0])

    # update feed
    print("Updating feed...")
    feed_manager = Feed()
    for i in range(0, len(new_communiques)):
        feed_manager.add_entry(new_communiques[i], pdfs_text[i])
    print(f"Done. Feed size is {feed_manager.get_total_feed_entries()}")

    # delete all feed entries
    print("Deleting old feed entries...")
    feed_manager.delete_old_entries()
    print(f"Done. Feed size is {feed_manager.get_total_feed_entries()}")


if __name__ == "__main__":
    main()
