from bs4 import BeautifulSoup
from scraper.request_helper import request
from models.communique import Communique
from utils import clean_string

BASE_URL = 'https://education.govmu.org'
SCHOLARSHIP_URL = BASE_URL + ("/Pages/Downloads/Scholarships"
                              "/Scholarships-for-Mauritius-Students.aspx")


def get_all_communiques(limit=0) -> list[Communique]:
    """
    Returns a list of all communiques found on the scholarship website.

    Read `docs/SCRAPING_NOTES.md` for more details on how scraping was done.

    Args:
        limit (int, optional): Maximum number of communiques to be
        returned. Defaults to 0 which means no limit.

    Returns:
        list[Communique]: A list of communique objects.
    """
    if limit < 0:
        raise SystemExit("Invalid limit of communiques.")
    all_communiques = []
    soup = BeautifulSoup(request(SCHOLARSHIP_URL).text, 'lxml')
    table_rows = soup.find('table').find_all('tr')

    for row in table_rows:
        # ignore header, footer, and empty rows
        if (row.find('td') is None) or (row.find('a') is None):
            continue

        # create a new communique object
        current_communique = Communique()

        # extract columns in current row
        columns = row.find_all('td')

        # if row has 2 columns then save closing date if any.
        if (len(columns) == 2):
            current_communique.closing_date = clean_string(
                columns[1].text)  # result may be empty

        # set communique title to the text content of first anchor tag
        current_communique.title = clean_string(columns[0].
                                                find('a').text)

        # The first anchor tag in each row is the scholarship name,
        if (current_communique.title == ""):
            current_communique.title = clean_string(columns[0].text)

        # create list of links present in first column of current row
        all_anchor_tags = columns[0].find_all('a')
        all_urls = []
        for tag in all_anchor_tags:
            url = BASE_URL + tag['href']
            if url not in all_urls:  # prevent duplicates
                all_urls.append(url)
        current_communique.urls = all_urls

        all_communiques.append(current_communique)

        # check if limit reached
        if (len(all_communiques) == limit):
            return all_communiques

    return all_communiques
