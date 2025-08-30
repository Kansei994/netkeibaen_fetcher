import requests
from pprint import pprint
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_detail(horse_id: str) -> str | None:
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

    data = soup.find("div", class_="ProfileDataTable HorseDataTable")

    horse_data = {}
    if data:
        for row in data.find_all("tr"):
            cols = row.find_all(["th", "td"])
            if len(cols) != 2:
                continue
            key = cols[0].get_text(strip=True)

            if key == "Dam":
                links = cols[1].find_all("a")
                if links:
                    horse_data["Dam"] = links[0].get_text(strip=True)
                    if len(links) > 1:
                        horse_data["Damsire"] = links[1].get_text(strip=True)
                else:
                    horse_data["Dam"] = cols[1].get_text(strip=True)
                continue  # skip normal processing

            for br in cols[1].find_all("br"):
                br.replace_with(", ")
            value = cols[1].get_text(strip=True)

            if key in ["Siblings", "Awards"]:
                value = [v.strip() for v in value.split(",") if v.strip()]

            horse_data[key] = value

    for k, v in horse_data.items():
        if isinstance(v, list):
            print(f"{k}:")
            for item in v:
                print(f"  - {item}")
        else:
            print(f"{k}: {v}")

    
    return None