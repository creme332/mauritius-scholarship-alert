# mauritius-scholarship-alert

 Stay up-to-date with the latest scholarships posted on govmu website.

![GIF](gifs/gif1.gif)

[▶ Live Preview]()

# 🚀Features
- Receive notification as soon as a new scholarship drops.
- Receive reminder a couple of days before closing date.
- Filtering options

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
- [ ] Use Github Workflow for automatic scraping. [Blog here](https://yasoob.me/posts/github-actions-web-scraper-schedule-tutorial/)
- limit access to api with this [method](https://www.youtube.com/watch?v=cRFM5AcfcPQ&ab_channel=InfoTechWARforCoding)


- [ ] Build an API.

- [ ] Make website responsive.
- [ ] Add sitemap + request indexing.
- [ ] Add project social media preview.
- [x] Add requirements.txt file

### ✔ Done
