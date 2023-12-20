import asyncio
import httpx
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


async def request_all(url_list: list[str]) -> list[requests.Response]:
    """Uses asynchronous programming to make parallel requests to server.

    Args:
        url_list (list): A list of URLS which must be requested

    Returns:
        list: Corresponding list of responses
    """

    #  Read : https://www.python-httpx.org/advanced/
    limits = httpx.Limits(max_keepalive_connections=10, max_connections=50)
    timeout = httpx.Timeout(10.0, connect=60.0)
    transport = httpx.AsyncHTTPTransport(retries=100)

    async with httpx.AsyncClient(transport=transport, limits=limits,
                                 timeout=timeout) as client:
        tasks = (client.get(url, follow_redirects=True) for url in url_list)
        responses = await asyncio.gather(*tasks, return_exceptions=True)
    return responses


def request(url: str) -> requests.Response:
    """
    Returns a response after requesting a URL.

    Args:
        url (str): A valid URL. Eg: `https://stackoverflow.com/`.

    Raises:
        SystemExit: Connection error.
        SystemExit: Invalid status code.
        SystemExit: Any other exceptions.

    Returns:
        requests.Response
    """
    HEADERS = {
        'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko)'
                       ' Chrome/75.0.3770.142 Safari/537.36')
    }
    # if we want to get the headers we sent the server,
    # print (makeRequest(url).request.headers)

    # https://stackoverflow.com/a/47475019/17627866
    session = requests.Session()
    session.headers.update(HEADERS)

    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        r = session.get(url)
    except requests.exceptions.ConnectionError as e:
        raise SystemExit(f"Connection error for {url}", e)
    except Exception as e:
        raise SystemExit(f"request({url})failed. Exception :", e)
    else:
        if (r.status_code == 200):  # valid response
            return r
        raise SystemExit(
            f"Invalid status code when requesting PDF : {r.status_code}",
            f"\n URL : {url}")
