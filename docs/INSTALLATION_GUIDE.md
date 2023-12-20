# Installation Guide

## For personal use
Follow the instructions in this section if you only want to use the project without installing the project. If you setup the project locally, follow [next section]().

### Prerequisites
- A Github account.
- App password for your gmail account

### Instructions
1. Fork the repository.
1. Enable two-factor authentication on your Gmail account if not already enabled.
2. Create an [App Password](https://itsupport.umd.edu/itsupport/?id=kb_article_view&sysparm_article=KB0015112&sys_kb_id=76433076dbdf8c904cb035623996194b&spa=1) for your account. Keep a copy of this password.
3. Create two [Github repository secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) named  `EMAIL_PASSCODE` and `SENDER_EMAIL_ADDRESS` respectively. `EMAIL_PASSCODE` should contain your newly created gmail app password and `SENDER_EMAIL_ADDRESS` should contain the corresponding gmail account. Do not include quotation marks in text box given.
    ![github secret image](../assets/githubsecret.png)
4. The project will now run automatically through Github Actions.
> 🔴 **Note**: Never use your gmail account password as the `EMAIL_PASSCODE` even though it works. The value `EMAIL_PASSCODE` must not be shared with anyone and must not be present in the code.** 

## For local development
### Prerequisites
- Python 3.9
- Git
- App password for your gmail account

### Instructions
Clone repository:
  ```bash
  git clone git@github.com:creme332/mauritius-scholarship-alert.git
  ```

Move to root directory of project directory:
 ```bash
 cd mauritius-scholarship-alert
 ```

Create a virtual environment using a method of your choice and activate it. For example:
```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies in your virtual environment:
 ```
 pip install -r requirements.txt
 ```
Create a `.env` file in the root directory the project:
 ```bash
 EMAIL_PASSCODE = "your gmail app password"
 SENDER_EMAIL_ADDRESS = "your gmail email address"
 ```
Run `src/main.py` script:
```bash
python src/main.py
```

## Testing
Inside the root of the project, run `pytest` in terminal.