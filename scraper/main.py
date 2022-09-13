#!venv/bin/python3
import datetime
import json
from bs4 import BeautifulSoup
from schdef import Communique
from cleanstring import cleanString
from emailsender import sendEmail
from pdfreader import getPDFtext
from requestfunc import makeRequest

LAST_SCRAPED_COMMUNIQUE = {}  # communique since last time scraping was done
# file containing LAST_SCRAPED_COMMUNIQUE
DATABASE_FILE_PATH = "data/scrape.json"


def main():
    global LAST_SCRAPED_COMMUNIQUE
    # Initialise LAST_SCRAPED_COMMUNIQUE
    with open(DATABASE_FILE_PATH) as f:
        LAST_SCRAPED_COMMUNIQUE = json.load(f)

    # scrape website
    URL = "https://education.govmu.org/Pages/Downloads/Scholarships/Scholarships-for-Mauritius-Students.aspx"
    scrapeWebsite(makeRequest(URL).text)


def updateDatabase(communique_info):
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

        current_communique.urls = urls
        current_communique.closingDate = cleanString(closingDate_field.text)
        current_communique.timestamp = ('{:%Y-%m-%d %H:%M:%S}'.
                                        format(datetime.datetime.now()))
        newScholarshipsList.append(current_communique.title)

        if not firstrowfound:
            firstrowfound = True
            first_communique = current_communique.to_dict()

        # sendEmail(current_communique.title, getPDFtext(
        #     urls[0]), 'c34560814@gmail.com')
    # print updates
    print(len(newScholarshipsList), "new scholarships discovered !\n")
    print("\n\n".join(newScholarshipsList))

    # update database only if needed
    if (LAST_SCRAPED_COMMUNIQUE == {}):  # this is our first time scraping
        updateDatabase(first_communique)
    else:
        if (first_communique != {} and
                first_communique['title'] != LAST_SCRAPED_COMMUNIQUE['title']):
            # we have found at least 1 new scholarship
            updateDatabase(first_communique)


if __name__ == "__main__":
    main()
