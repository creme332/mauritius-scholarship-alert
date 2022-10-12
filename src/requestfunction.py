#!venv/bin/python3
import asyncio
import httpx
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


async def getResponses(URL_list):
    """Uses asynchronous programming to make requests to server. 

    Args:
        URL_list (list): A list of URLS which must be requested

    Returns:
        list: Corresponding list of responses
    """

    #  Read : https://www.python-httpx.org/advanced/
    limits = httpx.Limits(max_keepalive_connections=10, max_connections=50)
    timeout = httpx.Timeout(10.0, connect=60.0)
    transport = httpx.AsyncHTTPTransport(retries=100)

    async with httpx.AsyncClient(transport=transport, limits=limits, timeout=timeout) as client:
        tasks = (client.get(url, follow_redirects=True) for url in URL_list)
        responses = await asyncio.gather(*tasks, return_exceptions=True)
    return responses


def makeRequest(URL):
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }
    # if we want to get the headers we sent the server, print (makeRequest(url).request.headers)
    
    # https://stackoverflow.com/a/47475019/17627866
    session = requests.Session()
    session.headers.update(HEADERS)

    retry = Retry(connect=5, backoff_factor=0.5) # max number of retries = 5
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    try:
        r = session.get(URL)
    except Exception as e:
        raise SystemExit(e)
    else:
        if (r.status_code == 200):  # valid response
            return r
        raise SystemExit(
            "Invalid status code when requesting PDF : {r.status_code}", "\n URL : {URL}")


if __name__ == "__main__":
    print(makeRequest('https://education.govmu.org/Pages/Downloads/Scholarships/Scholarships-for-Mauritius-Students.aspx'))
