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

from trending_horses import get_trending_horses


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

def user_input():
    u_input = input("Please input trending for trending horses, or search for searching a horse: ")
    if u_input in ("Search").lower():
        result()
    elif u_input in ("Trending").lower():
        get_trending_horses()
    else:
        print("Invalid Input.")
    user_input()

user_input()