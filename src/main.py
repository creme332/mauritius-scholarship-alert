import json
import asyncio

from models.communique import Communique
from utils import extract_text, has_keyword
from emailer.emailer import Emailer
from reminder import send_reminders
from scraper.scraper import get_all_communiques
from scraper.request_helper import request_all
# * Uncomment lines below to measure code performance
# import cProfile
# import pstats


# path to file containing last scraped communique
DATABASE_FILE_PATH = "data/scrape.json"


def filter(all_communiques: list[Communique]) -> list[Communique]:
    new_communiques = []

    last_communique = {}  # communique since last time scraping was done
    with open(DATABASE_FILE_PATH) as f:
        last_communique = json.load(f)

    # compare last scraped communique with each communique in list
    # keep only communiques which are found before last communique in
    # all_communiques
    for communique in all_communiques:
        if communique.title == last_communique['title']:
            return new_communiques
        new_communiques.append(communique)

    return new_communiques


def main() -> None:
    # fetch all communiques from website
    all_communiques = get_all_communiques()

    # send reminders if any
    send_reminders(all_communiques)

    # filter out communiques which were already scraped before
    # to get only new scholarships
    all_communiques = filter(all_communiques)

    print("Number of new scholarships =", len(all_communiques))

    # if no new communiques found, exit
    if (len(all_communiques) == 0):
        return

    # extract communique titles
    email_titles = [c.title for c in all_communiques]

    # * NOTE: each communique has at least 1 url
    # extract first url for each communiques
    pdf_urls = [c.urls[0] for c in all_communiques]

    # request pdfs
    pdf_responses = asyncio.run(request_all(pdf_urls))

    # get the pdf text from each response
    pdfs_text = [extract_text(r) for r in pdf_responses]

    # For newly discovered scholarships, send emails
    emailer = Emailer()
    for i in range(0, min(emailer.EMAIL_LIMIT, len(email_titles))):
        if (pdf_responses[i].status_code == 200 and
                has_keyword(pdfs_text[i])):
            emailer.send_new_scholarship(email_titles[i], pdfs_text[i])
    print(emailer.sent_count, "scholarship emails were sent!")


def save_recent_communique(new_communique: Communique) -> None:
    """Saves the most recently scraped communique to `scrape.json`

    Args:
        new_communique (Communique): The most recently recently scraped
        communique
    """
    with open(DATABASE_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(new_communique.to_dict(), f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()

    # * Uncomment lines below to measure code performance
    # with cProfile.Profile() as pr:
    #     main()

    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
