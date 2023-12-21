import asyncio

from communique_manager import CommuniqueManager
from utils import extract_text
from emailer.emailer import Emailer
from reminder import handle_reminders
from scraper.scraper import get_all_communiques
from scraper.request_helper import request_all

MANAGER = CommuniqueManager()


def main() -> None:
    global MANAGER

    # fetch all communiques from website
    print("Fetching all communiques")
    all_communiques = get_all_communiques()
    print("Done.")

    # send reminders if any
    handle_reminders(all_communiques)

    # filter out communiques which were already scraped before
    # to get only new communiques
    new_communiques = MANAGER.get_new_communiques(all_communiques)

    print("Number of new communiques found =", len(new_communiques))

    # if no new communiques found, exit
    if (len(new_communiques) == 0):
        return

    print("Fetching PDF of each communique...")

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

    print("Done.")

    # For send emails
    print("Sending email...")
    emailer = Emailer()
    for i in range(0, min(emailer.EMAIL_LIMIT, len(new_communiques))):
        if new_communiques[i].match_user_interests():
            emailer.send_new_scholarship(new_communiques[i], pdfs_text[i])

    print("Done.")
    print(emailer.sent_count, "scholarship emails were sent!")

    # update last scraped communique
    MANAGER.save(new_communiques[0])


if __name__ == "__main__":
    main()
