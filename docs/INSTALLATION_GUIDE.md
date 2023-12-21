# Installation Guide
- [Installation Guide](#installation-guide)
  - [For personal use](#for-personal-use)
    - [Prerequisites](#prerequisites)
    - [Instructions](#instructions)
  - [For local development](#for-local-development)
    - [Prerequisites](#prerequisites-1)
    - [Instructions](#instructions-1)
  - [Testing](#testing)

## For personal use
Follow the instructions in this section if you only want to use the tool without installing the project locally. 

### Prerequisites
- A Github account
- A Gmail account

### Instructions
1. Fork the repository.
1. Enable two-factor authentication on your Gmail account if not already enabled.
2. Create an [App Password](https://itsupport.umd.edu/itsupport/?id=kb_article_view&sysparm_article=KB0015112&sys_kb_id=76433076dbdf8c904cb035623996194b&spa=1) for your account. Keep a copy of this password.
3. In your repository settings, create two [Github repository secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) named  `EMAIL_PASSCODE` and `SENDER_EMAIL_ADDRESS` respectively. `EMAIL_PASSCODE` should contain your newly created gmail app password and `SENDER_EMAIL_ADDRESS` should contain the corresponding gmail account. Do not include quotation marks in text box provided by Github.
    ![github secret image](../assets/githubsecret.png)
4. Everything is now setup and the scraper will run automatically through Github Actions.
> 🔴 **Note**: Never use your gmail account password as the `EMAIL_PASSCODE` even though it works. The value `EMAIL_PASSCODE` must not be shared with anyone and must not be present in the code.

## For local development
### Prerequisites
- Python 3.9
- Git
- A Gmail account

### Instructions
Clone the repository:
  ```bash
  git clone git@github.com:creme332/mauritius-scholarship-alert.git
  ```

Move to the root directory of the project:
 ```bash
 cd mauritius-scholarship-alert
 ```

Create a virtual environment using a method of your choice and activate it. For example:
```bash
python -m venv .venv
source .venv/bin/activate
```

Install the required dependencies in your virtual environment:
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
Inside the root directory of the project, run:
```
pytest
```