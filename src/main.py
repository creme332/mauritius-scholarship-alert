import asyncio
from communique_manager import CommuniqueManager
from utils import extract_text
from emailer.emailer import Emailer
from reminder import handle_reminders
from scraper.scraper import get_all_communiques
from scraper.request_helper import request_all
from feed import Feed


def reset_data() -> None:
    """
    Call this function when you messed up and you want to reset everything.
    The following actions are taken:
    - The atom feed will be erased and initialized with the 5
    latest scholarships.
    - The data in scrape.json will get updated.
    - No emails are sent.
    - No reminders are sent.
    """
    feed_manager = Feed()
    communique_manager = CommuniqueManager()
    SIZE = 5

    # erase last scraped communique in scrape.json
    communique_manager.reset_last_communique()

    # erase atom feed info
    feed_manager.reset()

    # fetch the 5 latest scholarships and their PDF text
    all_communiques = get_all_communiques(SIZE)
    communique_manager.save(all_communiques[0])

    pdf_urls = [c.urls[0] for c in all_communiques]
    pdf_responses = asyncio.run(request_all(pdf_urls))
    pdfs_text = [extract_text(r)
                 for r in pdf_responses if r.status_code == 200]

    # populate atom feed
    for i in range(len(all_communiques) - 1, -1, -1):
        feed_manager.add_entry(all_communiques[i], pdfs_text[i])


def main() -> None:
    """
    Driver function for program.
    """
    communique_manager = CommuniqueManager()

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
    new_communiques = communique_manager.get_new_communiques(all_communiques)

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
    user_interests = communique_manager.get_user_interests()

    # For send emails
    print("Sending email...")
    emailer = Emailer()
    for i in range(0, min(emailer.EMAIL_LIMIT, len(new_communiques))):
        if new_communiques[i].match_user_interests(user_interests):
            emailer.send_new_scholarship(new_communiques[i], pdfs_text[i])

    print(f"Done. {emailer.sent_count} scholarship emails were sent!")

    # update last scraped communique
    communique_manager.save(new_communiques[0])

    # update feed
    print("Updating feed...")
    feed_manager = Feed()

    # feed entries must be added in chronological order where
    # the first entry is the latest one
    for i in range(len(new_communiques) - 1, -1, -1):
        feed_manager.add_entry(new_communiques[i], pdfs_text[i])
    print(f"Done. Feed size is {feed_manager.get_total_feed_entries()}")

    # delete all feed entries
    print("Deleting old feed entries...")
    feed_manager.delete_old_entries()
    print(f"Done. Feed size is {feed_manager.get_total_feed_entries()}")


if __name__ == "__main__":
    main()
