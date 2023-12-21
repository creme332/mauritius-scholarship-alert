import asyncio

from communique_manager import CommuniqueManager
from utils import extract_text, has_keyword
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
    new_communiques = MANAGER.filter_new(all_communiques)

    print("Number of new scholarships =", len(new_communiques))

    # if no new communiques found, exit
    if (len(new_communiques) == 0):
        return

    print("Fetching PDF...")

    # * NOTE: each communique has at least 1 url
    # extract first url for each communiques
    pdf_urls = [c.urls[0] for c in new_communiques]

    # request pdfs
    pdf_responses = asyncio.run(request_all(pdf_urls))

    # get the pdf text from each response
    pdfs_text = [extract_text(r) for r in pdf_responses]

    print("Done.")

    # For newly discovered scholarships, send emails
    print("Sending email...")
    emailer = Emailer()
    for i in range(0, min(emailer.EMAIL_LIMIT, len(new_communiques))):
        if (pdf_responses[i].status_code == 200 and
                has_keyword(pdfs_text[i])):
            emailer.send_new_scholarship(new_communiques[i], pdfs_text[i])

    print("Done.")
    print(emailer.sent_count, "scholarship emails were sent!")

    # update last scraped communique
    MANAGER.save(new_communiques[0])


if __name__ == "__main__":
    main()
