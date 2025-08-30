import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from horse_name import get_horse_name
from horse_name import label
from profile_detail import get_detail

from race_data import race_data
from pedigree import pedigree

from horse_search import find_id


def result():
    word = input("Horse Name: ")
    horse_id = find_id(word)
    print(get_horse_name(horse_id)) 
    print(label(horse_id))
    print(get_detail(horse_id))
    print(f"https://en.netkeiba.com/db/horse/{horse_id}/")

    race_data((horse_id))
    pedigree((horse_id))
    return 

result()