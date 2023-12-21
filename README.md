# 🔔 mauritius-scholarship-alert
![Build status of workflow](https://github.com/creme332/mauritius-scholarship-alert/actions/workflows/main.yml/badge.svg)

![mauritius scholarship alert logo](assets/logo.png)

Get notified by email each time a new scholarship communique is posted on the [Ministry of Education of Mauritius website](https://education.govmu.org/Pages/Downloads/Scholarships/Scholarships-for-Mauritius-Students.aspx).

The current government website, as of 2024, lacks an email subscription or an RSS feed or an API, requiring manual checks for new scholarship updates. This tool eliminates this hassle by automatically sending you an email notification whenever a scholarship is posted. Additionally, it offers advanced features beyond a standard RSS feed, including customizable filtering options and deadline reminders.

## Features
- Customizable email template
- Communique PDF included as email attachment
- Deadline reminders
- Filtering options
- Asynchronous programming for fast web scraping.
- Tested with pytest

## How it works
1. A scheduled CRON job runs a web scraper on a daily basis.
2. The script performs web scraping on the scholarship website to detect any new announcements or updates.
3. The PDF content of the communique is extracted and sent by email to you.
4. The most recent communique found is then saved in `data/scrape.json` for future reference.  

## Limitations
- Any images in the PDF will not be included in the email notification.


## To-do
- [ ] if website was an issue, save html of website to a file
- [ ] add images of email template to readme
- [ ] Test filter
- [ ] add image extraction with pypdf: https://github.com/py-pdf/pypdf/issues/2256
  - [ ] https://red-mail.readthedocs.io/en/v0.1.1/tutorials/body_content.html
  - [ ] https://www.developer.com/languages/displaying-and-converting-images-with-python/
- [ ] Build an API in express
- [ ] add excalidraw diagram explaining how it works
- [ ] Create a registration form so that anyone can subscribe for updates.
- [ ] update requirements.txt for all packages

## Changelog
- [x] use node 16 in github actions
- [x] Followed PEP8 convention
- [x] Added `docs` + pydocs
- [x] Add tests + workflow
- [x] Upgraded packages to fix security vulnerabilities
- [x] Re-structured project
## License
This project uses the MIT license.