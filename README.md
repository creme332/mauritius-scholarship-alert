# 🔔 mauritius-scholarship-alert
![Build status of workflow](https://github.com/creme332/mauritius-scholarship-alert/actions/workflows/main.yml/badge.svg)

![mauritius scholarship alert logo](assets/logo.png)

Get notified by email each time the Ministry of Education of Mauritius posts a new scholarship communique on its [website](https://education.govmu.org/Pages/Downloads/Scholarships/Scholarships-for-Mauritius-Students.aspx).

> ⚠ This project is not affiliated with the Ministry of Education of Mauritius. 

# 🚀Features
- Receive an email notification at most 12 hours after a new scholarship is posted.
- Option to filter scholarships by keyword.
- Option to receive an email reminder 3 days before the closing date of a specified scholarship.
- Asynchronous programming to speed up fetching of PDFs from website.

# ⚙ How it works
- Github Actions is used to automatically run `main.py` script every day.
 - The program scrapes the scholarship website and checks for any new communique. 
 - Newly discovered communiques are sent by email to you. Your own email address will be used to send you emails.
    ![Example of email](assets/emailgif.gif)

 - The most recent commnique found is then saved in `scrape.json` for future reference.

# ✍Usage
## Run with Github Actions 
The fastest way to get started is to fork this repository and follow the following instructions :
1. Create a [gmail app password](https://itsupport.umd.edu/itsupport/?id=kb_article_view&sysparm_article=KB0015112&sys_kb_id=76433076dbdf8c904cb035623996194b&spa=1). Keep a copy of this password.
2. Create two [Github repository secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) named  `EMAIL_PASSCODE` and `SENDER_EMAIL_ADDRESS` respectively. `EMAIL_PASSCODE` should contain your newly created gmail app password and `SENDER_EMAIL_ADDRESS` should contain the corresponding gmail account. Do not include quotation marks in text box given.
    ![github secret image](assets/githubsecret.png)

> ⚠ It is **NOT** recommended to use your gmail account password as the `EMAIL_PASSCODE` even though it works.

> ⚠ **The value `EMAIL_PASSCODE` must not be shared with anyone and must not be present in the code.** 

## Run locally without Github Actions
1. Clone repo.

    ```bash
    git clone git@github.com:creme332/mauritius-scholarship-alert.git
    ```

2. Install dependencies.
    ```
    pip install -r requirements.txt
    ```

3. Create a `.env` file with the following contents :

    ```bash
    EMAIL_PASSCODE = "your gmail app password"
    SENDER_EMAIL_ADDRESS = "your gmail email address"
    ```
4. Run `main.py` script.

## Filtering scholarships
By default filtering option is turned off. To turn on, enter keywords in `keywords.txt`. You will only be notified of scholarships matching **at least one of the keywords**.

For example, to be notified of only master's scholarships to the UK, your `keywords.txt` should look like this :
```
master's
uk
```
> 💡 Keywords may include country name, degree level, ...

> 💡 Keep `keywords.txt` empty to disable filtering.

## Enable reminders of scholarships' closing dates

Ensure that  `scholarships.txt` is empty if you do not want to receive any reminder of the closing date of scholarships.

To be reminded of the closing date of scholarships **3 days before its closing date**, enter the **exact name** of each communique on a new line in `scholarships.txt`. 

For example, to be reminded of the scholarship highlighted below, 

![screenshot of website highlighting one communique](assets/example.png)

Your `scholarships.txt` should contain :
```
​STATE OF MAURITIUS POSTGRADUATE SCHOLARSHIP SCHEME 2022/2023
```

If the communique field is multi-line with many links, enter the data from **only the first line**.

To be reminded of **all** scholarships, place only an asterisk `*` in the first line of `scholarships.txt`.

```
*
```

# 🤚 Limitations
- Up to 5 emails (excluding reminders) can be sent every 12 hours.

> ⚠ This limits the consequences of a program malfunction in the event of a major change to the scholarship website. In the worst case scenario, the program may send emails for all scholarships at once and you may get your gmail account banned. Change the email limit in the source code at your own risk.

- If you set your repository to private, Github Actions will give you only 2000 execution minutes per month. A public Github repository has no such limit. 
- The `main.py` script has a run duration of **25-60 seconds** on the  Ubuntu 2-core runner provided by Github.

For updated information about quotas :
- [Github Actions Quotas](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)
- [Gmail Quotas](https://support.google.com/a/answer/166852?hl=en)

# 📃License
 This project uses the MIT license.

# 🔨 To-Do
- [ ] Add unit tests + possibly a separate workflow
- [ ] Save all scraped data to Firestore
- [ ] Create a registration form so that anyone can subscribe for updates.

### ✔ Done
- [x] Remind me of approaching closing dates.
- [x] Option to filter scholarships by type
- [x] Add project social media preview.
- [x] Add automatic build passing/failed shield
- [x] Create new github secret for email
- [x] Try to reduce execution time : remove unused libraries, caching, optimise program, asyncio ...
