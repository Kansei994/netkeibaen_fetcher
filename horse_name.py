import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_horse_name(horse_id: str) -> str | None:
    url = f"https://en.netkeiba.com/db/horse/{horse_id}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://en.netkeiba.com/",
        "Connection": "keep-alive",
    }

    session = requests.Session()
    retry = Retry(
        total=3, backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"])
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))

    r = session.get(url, headers=headers, timeout=15)
    if r.status_code != 200:
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    h1 = soup.find("h1")
    if h1 and (name := h1.get_text(strip=True)):
        return name

    # 1Fallback
    og = soup.find("meta", attrs={"property": "og:title"})
    if og and og.get("content"):
        return og["content"].split("|")[0].strip()

    # 2Fallback
    if soup.title and soup.title.string:
        return soup.title.string.split("|")[0].strip()

    return None

def label(horse_id: str) -> str | None:
    url = f"https://en.netkeiba.com/db/horse/{horse_id}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://en.netkeiba.com/",
        "Connection": "keep-alive",
    }

    session = requests.Session()
    retry = Retry(
        total=3, backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"])
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))

    r = session.get(url, headers=headers, timeout=15)
    if r.status_code != 200:
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    hlabel = soup.find("div", class_="Data")

    print(hlabel.text)

    return None