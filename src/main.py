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


def filter_new(all_communiques: list[Communique]) -> list[Communique]:
    """
    Given a list of communiques ordered by closing date
    (oldest communique is last), return the communiques which were
    not encountered the last time the website was scraped.

    Args:
        all_communiques (list[Communique]): _description_

    Returns:
        list[Communique]: _description_
    """
    new_communiques = []

    # read last scraped communique from file
    # ! file is guaranteed to contain at least an empty dictionary
    last_scraped_communique = {}
    with open(DATABASE_FILE_PATH) as f:
        last_scraped_communique = json.load(f)

    # if website is being scraped for the first time, all communiques are new
    if not last_scraped_communique:
        return all_communiques

    # compare the last scraped communique with each communique
    # in all_communiques. keep only communiques which are found before
    # the last communique
    for communique in all_communiques:
        if communique.title == last_scraped_communique['title']:
            return new_communiques
        new_communiques.append(communique)

    return new_communiques


def main() -> None:
    # fetch all communiques from website
    all_communiques = get_all_communiques()

    # filter out communiques which were already scraped before
    # to get only new scholarships
    new_communiques = filter_new(all_communiques)

    # send reminders if any
    send_reminders(all_communiques)

    print("Number of new scholarships =", len(new_communiques))

    # if no new communiques found, exit
    if (len(new_communiques) == 0):
        return

    # update last scraped communique
    save_recent_communique(new_communiques[0])

    # extract communique titles
    email_titles = [c.title for c in new_communiques]

    # * NOTE: each communique has at least 1 url
    # extract first url for each communiques
    pdf_urls = [c.urls[0] for c in new_communiques]

    # request pdfs
    pdf_responses = asyncio.run(request_all(pdf_urls))

    # get the pdf text from each response
    pdfs_text = [extract_text(r) for r in pdf_responses]

    # ! TAKE filter.txt into consideration
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
