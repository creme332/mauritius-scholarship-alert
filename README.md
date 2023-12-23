# 🔔 mauritius-scholarship-alert
![Scraper status badge](https://github.com/creme332/mauritius-scholarship-alert/actions/workflows/main.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![logo](assets/logo.png)

Get notified by email each time a new scholarship communique is posted on the [Ministry of Education of Mauritius website](https://education.govmu.org/Pages/Downloads/Scholarships/Scholarships-for-Mauritius-Students.aspx).

The current government website unfortunately lacks an email subscription, an RSS feed, and an API, requiring manual checks for new scholarship updates. This tool eliminates this hassle by automatically sending you an email notification whenever a scholarship is posted. Additionally, it offers advanced features beyond a standard RSS feed, including customizable filtering options and deadline reminders.

[View email example 📧](assets/sample_email.pdf).

To get started, check out the [documentation](docs).

## Features
- Dynamic Atom feed
- Customizable email template
- Deadline reminders
- Filtering options
- Asynchronous programming for fast web scraping
- Tested with PyTest

## How it works
1. A scheduled CRON job runs a web scraper on a daily basis.
2. All communiques on the scholarship website are scraped.
3. If a new communique is detected,
   1. The PDF content of the communique is extracted
   2. An email is sent to user.
   3. Atom feed is updated.
4. Using the closing dates of all communiques scraped, reminders are sent by email to user.

## Limitations
- Any images in the PDF will not be included in the email notification.


## To-do
- [ ] add delay between each email sent
- [ ] add image extraction from pdf:
  - [ ] https://github.com/py-pdf/pypdf/issues/2256
  - [ ] https://red-mail.readthedocs.io/en/v0.1.1/tutorials/body_content.html
  - [ ] https://www.developer.com/languages/displaying-and-converting-images-with-python/
- [ ] build an API in express
- [ ] add excalidraw diagram explaining how it works
- [ ] create a registration form so that anyone can subscribe for updates.