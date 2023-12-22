# Configurations
- [Configurations](#configurations)
  - [Filtering scholarships](#filtering-scholarships)
  - [Deadline reminders](#deadline-reminders)
    - [Change deadline gap](#change-deadline-gap)
  - [Email limit](#email-limit)
  - [Scraping frequency](#scraping-frequency)
  - [Email templates](#email-templates)

## Filtering scholarships
By default, `interests.txt` contains `*` on its first line and you will be notified of all new scholarships.

To add a restriction, enter some keywords (one lowercase keyword per line) in `interests.txt`. You will only be notified of scholarships matching **at least one of the keywords**.

For example, to be notified of only master's scholarships to the UK, your `interests.txt` should look like this :
```
master's
uk
```
> 🔴 **Note:** Use lowercase for keywords and use only ASCII characters.

> 💡 Keywords may include country name, degree level, ...

> 💡 Add `*` on the **first** line of `interests.txt` to be notified of **all new communiques**.

## Deadline reminders
By default, `reminders.txt` contains `*` on its first line and you will be notified of the upcoming deadlines of all communiques 3 days before the deadline.

To disable reminders, `reminders.txt` shuold be empty.

To be reminded of the closing date of some scholarship **3 days before its closing date**, enter the **exact name** of the communique (as stored in `scrape.json`) on a new line in `reminders.txt`. 

For example, to be reminded of the scholarship highlighted below, 

![screenshot of website highlighting one communique](../assets/example.png)

The contents of `reminders.txt` should be:
```
​STATE OF MAURITIUS POSTGRADUATE SCHOLARSHIP SCHEME 2022/2023
```
> 🔴 **Note:**  Casing is important.

If the communique field is multi-line with many links, enter the data from **only the first line**.

### Change deadline gap
By default, you will receive a deadline reminders 3 days before the deadline. To change this value, edit `DEADLINE_GAP` in `reminder.py`.

## Email limit
Currently, up to 5 new scholarship emails and 5 reminders can be sent every 12 hours. This limits the consequences of a program malfunction in the event of a major change to the scholarship website. In the worst case scenario, the program may send emails for all scholarships at once and you may get your gmail account banned. You can modify this limit `EMAIL_LIMIT` in the `Emailer` class at your own risk.

## Scraping frequency
To change the frequency at which scraping takes place, change the following value in `.github/workflows/main.yml`:
```bash
  schedule:
    - cron: "0 */12 * * *" # Every 12 hours
```
The feed will be updated at the same rate.

## Email templates
You can configure the email templates in `src/emailer/templates`. Some knowledge of HTML and Jinja2 is required.