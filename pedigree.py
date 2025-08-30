import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os

import imgkit

def pedigree(horse_id: str) -> str | None:
    url = f"https://en.netkeiba.com/db/horse/ped/{horse_id}/"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    pedigree_table = soup.find("section", class_="Blood")
    if not pedigree_table:
        raise ValueError("Pedigree not found")

    html_content = str(pedigree_table)

    folder = "imagedata"
    os.makedirs(folder, exist_ok=True)  

    output_path = os.path.join(folder, f"{horse_id}_pedigree.png")
    
    imgkit.from_string(html_content, output_path)

