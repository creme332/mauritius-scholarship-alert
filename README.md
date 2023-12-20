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

## How it works
1. A scheduled CRON job runs a web scraper on a daily basis.
2. The script performs web scraping on the scholarship website to detect any new announcements or updates.
3. The PDF content of the communique is extracted and sent by email to you.
4. The most recent communique found is then saved in `data/scrape.json` for future reference.  

## Limitations
- Any images in the PDF will not be included in the email notification.
- If you set your repository to private, Github Actions will give you only 2000 execution minutes per month. A public Github repository has no such limit. 
- The `main.py` script has a run duration of **25-60 seconds** on the  Ubuntu 2-core runner provided by Github.

For updated information about quotas :
- [Github Actions Quotas](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)
- [Gmail Quotas](https://support.google.com/a/answer/166852?hl=en)

## To-do
    DEFAULT_GAP = 3  # numbers of days before closing date to send reminder
- [ ] Add type hinting to all functions
- [ ] if website was an issue, save html of website to a file
- [ ]create new branch and update implementation
- [ ] Fix empty email issue: Grant from Austria has an image embeded in pdf
- [ ] add images of email template
- [ ] rename text file to filters
- [ ] Send PDF file as email attachment: https://dev.to/seraph776/download-pdf-files-using-python-4064

- [ ] Add unit tests + possibly a separate workflow
- [ ] Build an API in express
- [ ] If communique missing, do not use old one.
- [ ] add excalidraw diagram explaining how it works
- [ ] create a simple website
- [ ] Create a registration form so that anyone can subscribe for updates.

## Changelog
- [x] use node 16 in github actions
- [x] Followed PEP8 convention
- [x] Added `docs`
- [x] Re-structured project
## License
This project uses the MIT license.