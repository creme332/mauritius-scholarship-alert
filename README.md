# mauritius-scholarship-alert

Stay up-to-date with the latest scholarships for Mauritian students.

![GIF](gifs/gif1.gif)

[▶ Live Preview]()

# 🚀Features
- Receive an email notification each time a new scholarship drops.
- Receive reminder a couple of days before closing date.
- Filtering options
- Asynchronous programming, caching dependencies to speed up Github Actions

# How it works

 - Occasionally scrape govmu website using Github Actions.
 - Check for updates.
 - If update, update my website, send email and save update to `scrape.json`

# Why not use the govmu website directly ?
- Inconsistent html. (one bullet point had an anchor   tag to it, strong tag nested in anchor or anchor nested in strong tag)
- govmu data contains erratic line breaks, lf/cr chars which had to be removed.
- No filtering options available.
- You will have to manually check the website for updates.
- Inconsistent capitalisation.

# 📌 Attributions
Resource | Source
---|---
resource| owner

# Assumptions when scraping 
- The first anchor tag in each row is the scholarship name.  (This is not true for Queen Elizabeth)

# 🔨 To-Do
- [ ] Save all scraped data to firestore
- [ ] Try to reduce execution time : include all code in one file, remove unused libraries, caching, optimise program, asyncio ...

- [ ] be more stringent when comparing communique
- [ ] Build an API.
pip cache is not found

- [ ] Make website responsive.
- [ ] Add sitemap + request indexing.
- [ ] Add project social media preview.
- [x] Add requirements.txt file
- [x] Use Github Workflow for automatic scraping. [Blog here](https://yasoob.me/posts/github-actions-web-scraper-schedule-tutorial/)
- limit access to api with this [method](https://www.youtube.com/watch?v=cRFM5AcfcPQ&ab_channel=InfoTechWARforCoding)
### ✔ Done
