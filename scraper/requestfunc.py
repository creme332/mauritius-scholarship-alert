#!venv/bin/python3

import requests
def makeRequest(URL):
    HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    TIMEOUT = 100 # allow at most 100s to make request
    try:
        r = requests.get(URL, headers=HEADERS, timeout=TIMEOUT)
    except Exception as e:
        raise SystemExit(e)
    else:
        if (r.status_code == 200): # valid response
            return r
        raise SystemExit("Invalid status code when requesting PDF : {r.status_code}", "\n URL : {URL}")

if __name__ == "__main__":
    makeRequest('hello.xyz')