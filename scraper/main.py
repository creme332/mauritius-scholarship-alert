#!venv/bin/python3

import requests
from bs4 import BeautifulSoup
from schdef import Communique
from cleanstring import cleanString
import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("scraper/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def getScholarships():
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    URL = "https://education.govmu.org/Pages/Downloads/Scholarships/Scholarships-for-Mauritius-Students.aspx"
    BASE_URL = 'https://education.govmu.org'

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

        current_communique = Communique()
        current_communique.timestamp = ('{:%Y-%m-%d %H:%M:%S}'.
        format(datetime.datetime.now()))

        communique_field = row.find_all('td')[0]
        closingDate_field = row.find_all('td')[1]

        all_anchor_tags = communique_field.find_all('a')
        for tag in all_anchor_tags:
            current_communique.urls.append(BASE_URL + tag['href'])

        current_communique.title = cleanString(communique_field.find('a').text)
        current_communique.closingDate = cleanString(closingDate_field.text)
        db.collection('test').add(current_communique.to_dict())

        # print(current_communique.to_dict())
        # return
        # corner case for "Queen Elizabeth Commonwealth Scholarships for academic Year 2022/2023"
        # if (scholarship_name == ""):
        #     scholarship_name = cleanString(communique_field.text)

getScholarships()
