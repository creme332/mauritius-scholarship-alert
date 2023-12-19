import datetime
import json
import asyncio
from bs4 import BeautifulSoup

from communique import Communique
from utils import clean_string, extract_text, has_keyword
from emailer import Emailer
from request_helper import request, request_all
from reminder import must_send_reminder

# to measure code performance
# import cProfile
# import pstats

LAST_SCRAPED_COMMUNIQUE = {}  # communique since last time scraping was done
# file containing LAST_SCRAPED_COMMUNIQUE
DATABASE_FILE_PATH = "data/scrape.json"


def main():

    # Initialise LAST_SCRAPED_COMMUNIQUE
    global LAST_SCRAPED_COMMUNIQUE
    with open(DATABASE_FILE_PATH) as f:
        LAST_SCRAPED_COMMUNIQUE = json.load(f)

    # get html code of website
    URL = ("https://education.govmu.org/Pages/Downloads/Scholarships"
           "/Scholarships-for-Mauritius-Students.aspx")
    RESPONSE_TEXT = request(URL).text

    # get html code of rows in first table on website
    SOUP = BeautifulSoup(RESPONSE_TEXT, 'lxml')
    TABLE_ROWS = SOUP.find('table').find_all('tr')

    # obtain communique titles and main pdf urls
    return_values = extract_main_info(TABLE_ROWS)
    email_titles = return_values[1]  # new communique title
    pdf_urls = return_values[0]

    # request pdfs
    responses = asyncio.run(request_all(pdf_urls))

    # get the pdf text from each response
    pdfs_text = []
    skipped_responses = []
    for res in responses:
        if res.status_code == 200:
            pdfs_text.append(extract_text(res))
        else:
            pdfs_text.append("")
            skipped_responses.append(res)

    if (len(skipped_responses) > 0):
        print("Skipped responses\n", "\n".join(skipped_responses))

    # For newly discovered scholarships, send emails
    emailer = Emailer()
    for i in range(0, min(emailer.EMAIL_LIMIT, len(email_titles))):
        if (responses[i].status_code == 200 and
                has_keyword(pdfs_text[i])):
            emailer.send_new_scholarship(email_titles[i], pdfs_text[i])
    print(emailer.sent_count, "scholarship emails were sent!")

    # Check closing dates of all scholarships and send reminders if necessary
    send_reminders(TABLE_ROWS)


def update_database(communique_info):
    """Update the contents of in scrape.json

    Args:
        communique_info (dictionary): A dictionary with all
         relevant details of a communique
    """
    with open(DATABASE_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(communique_info, f, ensure_ascii=False, indent=4)


def extract_main_info(table_rows):
    """Returns a list of communique titles and pdf urls for communiques
    which have not been scraped before

    Args:
        table_rows (html): A list of the html code for each table row

    Returns:
        2D list: First inner list is for titles and second inner
        list is for pdf urls.
    """
    BASE_URL = 'https://education.govmu.org'  # base url for pdf docs
    first_row_found = False
    first_communique = {}
    global LAST_SCRAPED_COMMUNIQUE

    newScholarshipsList = []  # list of new scholarships discovered
    pdf_urls = []  # pdf urls which must be requested
    email_titles = []

    for row in table_rows:
        if row.find('td') is None:  # ignore header and footer rows
            continue
        if row.find('a') is None:  # ignore empty rows
            continue
        columns = row.find_all('td')

        current_communique = Communique()
        communique_field = columns[0]

        closingDateFound = False
        if (len(columns) == 2):
            closingDateFound = True
            closingDate_field = row.find_all('td')[1]

        current_communique.title = clean_string(communique_field.
                                                find('a').text)

        # The first anchor tag in each row is the scholarship name,
        #  except for QEC scholarship
        # corner case for communique similar to QEC
        if (current_communique.title == ""):
            current_communique.title = clean_string(communique_field.text)

        # if we encounter a previously scraped communique, exit
        if (LAST_SCRAPED_COMMUNIQUE != {} and
                current_communique.title == LAST_SCRAPED_COMMUNIQUE['title']):
            break

        # create list of links present in current communique
        all_anchor_tags = communique_field.find_all('a')
        urls = []
        for tag in all_anchor_tags:
            urls.append(BASE_URL + tag['href'])

        pdf_urls.append(urls[0])
        email_titles.append(current_communique.title)

        current_communique.urls = urls

        # if communique has no closing date, choose the closing
        # date of the last scraped communique
        if (closingDateFound):
            current_communique.closingDate = clean_string(
                closingDate_field.text)
        else:
            old_date = LAST_SCRAPED_COMMUNIQUE['closingDate']
            current_communique.closingDate = old_date

        current_communique.timestamp = ('{:%Y-%m-%d %H:%M:%S}'.
                                        format(datetime.datetime.now()))
        newScholarshipsList.append(current_communique.title)

        if not first_row_found:
            first_row_found = True
            first_communique = current_communique.to_dict()

    # print updates
    print(len(newScholarshipsList), "new scholarships found on website !")
    if (len(newScholarshipsList) > 0):
        print("\n\n".join(newScholarshipsList))

    # update database only if needed
    if (LAST_SCRAPED_COMMUNIQUE == {}):  # this is our first time scraping
        update_database(first_communique)
    else:
        if (first_communique != {} and
                first_communique['title'] != LAST_SCRAPED_COMMUNIQUE['title']):
            # we have found at least 1 new scholarship
            update_database(first_communique)
    return [pdf_urls, email_titles]


def send_reminders(table_rows):
    """Sends reminders (if any) for active communiques. An active
    communique is a communique currently displayed on the scholarship
    website.

    Args:
        table_rows (html): A list of the html code for each table row
    """
    emailer = Emailer()
    for row in table_rows:
        # ignore header, footer, empty rows
        if (row.find('td') is None) or (row.find('a') is None):
            continue

        # ignore communique with missing fields
        if (len(row.find_all('td')) == 1):
            continue

        current_communique = Communique()
        communique_field = row.find_all('td')[0]
        closingDate_field = row.find_all('td')[1]

        current_communique.closingDate = clean_string(closingDate_field.text)
        current_communique.title = clean_string(
            communique_field.find('a').text)
        if (current_communique.title == ""):
            current_communique.title = clean_string(communique_field.text)

        if must_send_reminder(current_communique.title,
                              current_communique.closingDate):
            emailer.send_reminder(current_communique.title)
    print(emailer.sent_count, "closing dates reminders were sent !")


if __name__ == "__main__":
    main()
    # with cProfile.Profile() as pr:
    #     main()

    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
