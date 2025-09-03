from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import re



def get_trending_horses(wait_time: int = 3):
    URL = "https://en.netkeiba.com/db/horse/ranking_list.html?hr=ninki&sort=daily"
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    driver.get(URL)
    time.sleep(wait_time)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    entries = [a.get_text(" ", strip=True) for a in soup.select("#horse_ranking a")]

    pattern = re.compile(
        r"^(\d+)"              # rank
        r"([A-Za-z\s]+)"       # horse name
        r"(\d+[cfhm])"         # age + sex
        r"\s*([a-z\s]+)"       # color
        r"([A-Z]\.[A-Za-z]+)"  # trainer
        r"([A-Za-z]+)"         # stable 
        r"(\d+)"               # views
    )

    for entry in entries:
        match = pattern.match(entry.strip().replace("views", "").strip())
        if not match:
            print(entry)
        else:
            rank, name, age_sex, color, trainer, stable, views = match.groups()
            print(
                f"{rank}. {name.strip()} — {age_sex}, {color.strip()} "
                f"— Trainer: {trainer} — Stable: {stable} "
                f"— {views} views"
            )

if __name__ == "__main__":
    get_trending_horses()
