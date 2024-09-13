import requests
from settings import *


def check_if_clan_exists(tag):
    requestURL = f"{clanRequestURL}{tag}"
    response = requests.get(requestURL)  # , headers={"Authorization": "Bearer " + apiKey})
    if response.status_code == 200:
        #info = response.json()
        return True  #info["name"]
    else:
        return False


def get_clan_name(tag):
    requestURL = f"{clanRequestURL}{tag}"
    response = requests.get(requestURL)
    info = response.json()
    return info["name"]