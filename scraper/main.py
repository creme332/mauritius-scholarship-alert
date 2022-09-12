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
DATABASE_FILE_PATH = "data/scrape.json" # file containing LAST_SCRAPED_COMMUNIQUE

# For testing purposes
# def addToTestDB(communique_info):
#     TEST_FILE_PATH =  "data/test.json"
#     with open(TEST_FILE_PATH, 'a', encoding='utf-8') as f:
#         json.dump(communique_info, f, ensure_ascii=False, indent=4)

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
    BASE_URL = 'https://education.govmu.org' # base url for pdf docs
    firstrowfound = False
    first_communique = {}
    global LAST_SCRAPED_COMMUNIQUE

    soup = BeautifulSoup(RESPONSETEXT, 'lxml')

    # There are 2 tables on the page. Only the first one is important.
    # We are scraping the newest rows/scholarships first
    table = soup.find('table')
    table_rows = table.find_all('tr')

    count = 0
    for row in table_rows:
        if row.find('td') is None:  # ignore header and footer rows
            continue
        if row.find('a') is None:  # ignore empty rows
            continue

        current_communique = Communique()
        communique_field = row.find_all('td')[0]
        closingDate_field = row.find_all('td')[1]

        current_communique.title = cleanString(communique_field.find('a').text)
        # corner case for "Queen Elizabeth Commonwealth Scholarships for academic Year 2022/2023"
        if (current_communique.title == ""):
            current_communique.title = cleanString(communique_field.text)

        # check if we are done scraping all new communique
        if (current_communique.title == LAST_SCRAPED_COMMUNIQUE['title']):
            if(first_communique != {}):
                # we found at least 1 new scholarship
                updateDatabase(first_communique)
            break

        # keep scraping
        all_anchor_tags = communique_field.find_all('a')
        urls = []
        for tag in all_anchor_tags:
            urls.append(BASE_URL + tag['href'])

        current_communique.urls = urls
        current_communique.closingDate = cleanString(closingDate_field.text)
        current_communique.timestamp = ('{:%Y-%m-%d %H:%M:%S}'.
                                        format(datetime.datetime.now()))
        count += 1

        if not firstrowfound:
            firstrowfound = True
            first_communique = current_communique.to_dict()

        print(current_communique.title, "\n")
        sendEmail(current_communique.title, getPDFtext(urls[0]),'c34560814@gmail.com')
    print(count, "new scholarships discovered !")

if __name__ == "__main__":
    main()