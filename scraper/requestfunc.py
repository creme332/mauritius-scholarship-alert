#!venv/bin/python3
import asyncio
import httpx
import requests

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
    # DEPRECATED FUNCTION
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