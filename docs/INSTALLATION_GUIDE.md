# Installation Guide
## Run with Github Actions 
The fastest way to get started is to fork this repository and follow the following instructions :
1. Create a [gmail app password](https://itsupport.umd.edu/itsupport/?id=kb_article_view&sysparm_article=KB0015112&sys_kb_id=76433076dbdf8c904cb035623996194b&spa=1). Keep a copy of this password.
2. Create two [Github repository secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) named  `EMAIL_PASSCODE` and `SENDER_EMAIL_ADDRESS` respectively. `EMAIL_PASSCODE` should contain your newly created gmail app password and `SENDER_EMAIL_ADDRESS` should contain the corresponding gmail account. Do not include quotation marks in text box given.
    ![github secret image](assets/githubsecret.png)

> ⚠ It is **NOT** recommended to use your gmail account password as the `EMAIL_PASSCODE` even though it works.

> ⚠ **The value `EMAIL_PASSCODE` must not be shared with anyone and must not be present in the code.** 

## Run locally without Github Actions
1. Clone repo:
    ```bash
    git clone git@github.com:creme332/mauritius-scholarship-alert.git
    ```
2. Create a virtual environment and activate it.
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Create a `.env` file with the following contents:
    ```bash
    EMAIL_PASSCODE = "your gmail app password"
    SENDER_EMAIL_ADDRESS = "your gmail email address"
    ```
5. Run `src/main.py` script.

