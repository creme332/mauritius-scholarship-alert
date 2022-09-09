#!venv/bin/python3

import requests
from bs4 import BeautifulSoup


def getScholarships():

    def cleanName(name):
        """Normalize scholarship name by getting rid of special characters
        like line feed, carriage return, ...

        Args:
            name (string): _description_

        Returns:
            string: _description_
        """
        NON_BREAK_SPACE_CHAR = u'\xa0'
        LF_CHAR = u'\n'  # line feed
        CR_CHAR = u'\r'  # carriage return
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
        count += 1
        if (row.find('td') is not None):  # ignore header and footer
            if row.find('a') is None:  # ignore empty rows
                continue
            name = cleanName(row.find('a').text)
            if (name != ""):
                print(count, " ", name, "\n")

getScholarships()