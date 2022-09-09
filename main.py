#!venv/bin/python3

import requests
from bs4 import BeautifulSoup


def getScholarships():

    def cleanString(name):
        """Normalize scholarship name by getting rid of special characters
        like line feed, zero width space, ...

        Args:
            name (string): original scholarship name directly from html

        Returns:
            string: Clean name
        """
        NON_BREAK_SPACE_CHAR = u'\xa0'
        LF_CHAR = u'\n'  # line feed
        EOL_CHAR = u'\r\n'  # end of line
        ZERO_WIDTH_SPACE = u'\u200b'

        name = name.strip()
        name = name.replace(EOL_CHAR, ' ')
        name = name.replace(NON_BREAK_SPACE_CHAR, ' ')
        name = name.replace(ZERO_WIDTH_SPACE, '')
        name = name.replace(LF_CHAR, '')

        return name.strip()
        # return name.strip().split(' ')
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    URL = "https://education.govmu.org/Pages/Downloads/Scholarships/Scholarships-for-Mauritius-Students.aspx"

    r = requests.get(URL, headers=HEADERS)
    if (r.status_code != 200):
        print("ERROR : Failed to request website")
        return

    soup = BeautifulSoup(r.text, 'lxml')
    # There are 2 tables on the page. Only the first one is important.
    table = soup.find('table')
    table_rows = table.find_all('tr')

    count = 0
    for row in table_rows:
        if row.find('td') is None:  # ignore header and footer rows
            continue
        if row.find('a') is None:  # ignore empty rows
            continue

        communique_column = row.find_all('td')[0]
        closingDate_column = row.find_all('td')[1]

        scholarship_name = cleanString(communique_column.find('a').text)
        closing_date = cleanString(closingDate_column.text)

        # corner case for "Queen Elizabeth Commonwealth Scholarships for academic Year 2022/2023"
        if (scholarship_name == ""):
            scholarship_name = cleanString(communique_column.text)

        count += 1
        print(count, " ", scholarship_name, "||", closing_date, "\n")


getScholarships()
