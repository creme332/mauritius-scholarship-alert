#!venv/bin/python3

import datetime
import json
import asyncio
from bs4 import BeautifulSoup

# my modules
from communiqueclass import Communique
from cleanstring import cleanString
from emailsender import sendEmail
from pdfreader import getPDFtext, validPDF
from requestfunction import makeRequest, getResponses
from reminder import mustSendReminder

# to measure code performance
# import cProfile
# import pstats

LAST_SCRAPED_COMMUNIQUE = {}  # communique since last time scraping was done
DATABASE_FILE_PATH = "data/scrape.json" # file containing LAST_SCRAPED_COMMUNIQUE

def main():

    # Initialise LAST_SCRAPED_COMMUNIQUE
    global LAST_SCRAPED_COMMUNIQUE
    with open(DATABASE_FILE_PATH) as f:
        LAST_SCRAPED_COMMUNIQUE = json.load(f)

    # get html code of website
    URL = "https://education.govmu.org/Pages/Downloads/Scholarships/Scholarships-for-Mauritius-Students.aspx"
    RESPONSETEXT = makeRequest(URL).text

    # get html code of rows in first table on website
    soup = BeautifulSoup(RESPONSETEXT, 'lxml')
    table_rows = soup.find('table').find_all('tr')

    # obtain communique titles and main pdf urls
    return_values = extractMainInfo(table_rows)
    email_titles = return_values[1]  # new communique title
    pdf_urls = return_values[0]

    # request pdfs
    responses = asyncio.run(getResponses(pdf_urls))

    # get the pdf text from each response
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

    # For newly discovered scholarships, send emails to myself
    # max number of emails that can be sent when main.py is run once.
    EMAIL_LIMIT = 5
    emails_sent_count = 0
    for i in range(0, min(EMAIL_LIMIT, len(email_titles))):
        if (responses[i].status_code == 200 and validPDF(all_pdfs[i])):
            sendEmail(email_titles[i], all_pdfs[i])
            emails_sent_count += 1
    print(emails_sent_count,"scholarship emails were sent!")

    # Check closing dates of all scholarships and send reminders if necessary
    sendReminders(table_rows)


def updateDatabase(communique_info):
    """Update the contents of in scrape.json

    Args:
        communique_info (dictionary): A dictionary with all
         relevant details of a communique
    """
    with open(DATABASE_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(communique_info, f, ensure_ascii=False, indent=4)


def extractMainInfo(table_rows):
    """Returns a list of communique titles and pdf urls for communiques 
    which have not been scraped before

    Args:
        table_rows (html): A list of the html code for each table row

    Returns:
        2D list: First inner list is for titles and second inner 
        list is for pdf urls.
    """
    BASE_URL = 'https://education.govmu.org'  # base url for pdf docs
    firstrowfound = False
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
    print(len(newScholarshipsList), "new scholarships found on website !")
    if(len(newScholarshipsList)>0):
        print("\n\n".join(newScholarshipsList))

    # update database only if needed
    if (LAST_SCRAPED_COMMUNIQUE == {}):  # this is our first time scraping
        updateDatabase(first_communique)
    else:
        if (first_communique != {} and
                first_communique['title'] != LAST_SCRAPED_COMMUNIQUE['title']):
            # we have found at least 1 new scholarship
            updateDatabase(first_communique)
    return [pdf_urls, email_titles]


def sendReminders(table_rows):
    """Sends reminders for communiques if needed

    Args:
        table_rows (html): A list of the html code for each table row
    """

    reminders_sent = 0 # number of reminders sent
    for row in table_rows:
        # ignore header, footer, empty rows
        if (row.find('td') is None) or (row.find('a') is None):
            continue

        current_communique = Communique()
        communique_field = row.find_all('td')[0]
        closingDate_field = row.find_all('td')[1]

        current_communique.closingDate = cleanString(closingDate_field.text)
        current_communique.title = cleanString(communique_field.find('a').text)
        if (current_communique.title == ""):
            current_communique.title = cleanString(communique_field.text)

        if mustSendReminder(current_communique.title, current_communique.closingDate):
            emailTitle = "URGENT : Deadline of scholarship approaching!"
            emailBody = f"""
            The deadline of "{current_communique.title}" is 3 days from now.
            View all details on website : https://education.govmu.org/Pages/Downloads/Scholarships/Scholarships-for-Mauritius-Students.aspx
            """
            sendEmail(emailTitle, emailBody)
            reminders_sent +=1 
    print(reminders_sent, "closing dates reminders were sent !")
if __name__ == "__main__":
    main()
    # with cProfile.Profile() as pr:
    #     main()

    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
