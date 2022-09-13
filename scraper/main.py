#!venv/bin/python3
import datetime
import json
from bs4 import BeautifulSoup
from schdef import Communique
from cleanstring import cleanString
from emailsender import sendEmail
from pdfreader import getPDFtext
from requestfunc import makeRequest, getResponses

import cProfile
import pstats
import asyncio

LAST_SCRAPED_COMMUNIQUE = {}  # communique since last time scraping was done
# file containing LAST_SCRAPED_COMMUNIQUE
DATABASE_FILE_PATH = "data/scrape.json"


def foo(pdf_urls, email_titles):
    responses = asyncio.run(getResponses(pdf_urls))
    all_pdfs = []
    skipped_responses = []

    for res in responses:
        if res.status_code == 200:
            all_pdfs.append(getPDFtext(res))
        else:
            all_pdfs.append("")
            skipped_responses.append(res)

    if (len(skipped_responses) > 0):
        print("Skipped responeses\n", "\n".join(skipped_responses))
    return
    # send an email to myself
    for i in range(0, len(email_titles)):
        if (responses[i].status_code == 200):
            print(email_titles[i])
            # sendEmail(email_titles[i], all_pdfs[i], 'c34560814@gmail.com')
            # await asyncio.sleep(1)


def main():
    global LAST_SCRAPED_COMMUNIQUE
    # Initialise LAST_SCRAPED_COMMUNIQUE
    with open(DATABASE_FILE_PATH) as f:
        LAST_SCRAPED_COMMUNIQUE = json.load(f)

    # scrape website
    URL = "https://education.govmu.org/Pages/Downloads/Scholarships/Scholarships-for-Mauritius-Students.aspx"
    r = scrapeWebsite(makeRequest(URL).text)
    email_titles = r[1]
    pdf_urls = r[0]
    foo(pdf_urls, email_titles)


def updateDatabase(communique_info):
    return
    with open(DATABASE_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(communique_info, f, ensure_ascii=False, indent=4)


def scrapeWebsite(RESPONSETEXT):
    BASE_URL = 'https://education.govmu.org'  # base url for pdf docs
    firstrowfound = False
    first_communique = {}
    global LAST_SCRAPED_COMMUNIQUE

    soup = BeautifulSoup(RESPONSETEXT, 'lxml')

    # There are 2 tables on the page. Only the first one is important.
    # The first table contains communiques sorted by date (earliest first)
    table = soup.find('table')
    table_rows = table.find_all('tr')

    newScholarshipsList = []  # list of new scholarships discovered
    pdf_urls = []  # pdf urls which must be requested
    email_titles = []

    for row in table_rows:
        if row.find('td') is None:  # ignore header and footer rows
            continue
        if row.find('a') is None:  # ignore empty rows
            continue

        current_communique = Communique()
        communique_field = row.find_all('td')[0]
        closingDate_field = row.find_all('td')[1]

        current_communique.title = cleanString(communique_field.
                                               find('a').text)

        # The first anchor tag in each row is the scholarship name,
        #  except for QEC scholarship
        # corner case for communique similar to QEC
        if (current_communique.title == ""):
            current_communique.title = cleanString(communique_field.text)

        # if we encounter a previously scraped communique, exit
        if (LAST_SCRAPED_COMMUNIQUE != {} and current_communique.title == LAST_SCRAPED_COMMUNIQUE['title']):
            break

        # create list of links present in current communique
        all_anchor_tags = communique_field.find_all('a')
        urls = []
        for tag in all_anchor_tags:
            urls.append(BASE_URL + tag['href'])

        pdf_urls.append(urls[0])
        email_titles.append(current_communique.title)

        current_communique.urls = urls
        current_communique.closingDate = cleanString(closingDate_field.text)
        current_communique.timestamp = ('{:%Y-%m-%d %H:%M:%S}'.
                                        format(datetime.datetime.now()))
        newScholarshipsList.append(current_communique.title)

        if not firstrowfound:
            firstrowfound = True
            first_communique = current_communique.to_dict()

    # print updates
    print(len(newScholarshipsList), "new scholarships discovered !\n")
    # print("\n\n".join(newScholarshipsList))

    # update database only if needed
    if (LAST_SCRAPED_COMMUNIQUE == {}):  # this is our first time scraping
        updateDatabase(first_communique)
    else:
        if (first_communique != {} and
                first_communique['title'] != LAST_SCRAPED_COMMUNIQUE['title']):
            # we have found at least 1 new scholarship
            updateDatabase(first_communique)
    return [pdf_urls, email_titles]


if __name__ == "__main__":
    # main()
    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    # stats.dump_stats(filename='needs_profiling.prof')
