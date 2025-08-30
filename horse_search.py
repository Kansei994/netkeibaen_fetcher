import requests
from bs4 import BeautifulSoup

def find_id(word: str) -> str | None:
    url = "https://en.netkeiba.com/db/horse/horse_list.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://en.netkeiba.com/",
        "Upgrade-Insecure-Requests": "1",
    }
    data = {
        "type": "db",
        "encode": "",
        "word": word,
        "submit": "Search"
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    first_result = soup.select_one('li.fc a')

    if first_result and 'href' in first_result.attrs:
        # Extract the horse ID
        return first_result['href'].strip("/").split("/")[-1]
    else:
        print("Couldn't find horse")
    return None

