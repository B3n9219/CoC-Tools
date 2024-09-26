import requests
from config.config import config


def check_if_clan_exists(tag):
    requestURL = f"{config["clan_request_url"]}{tag}"
    response = requests.get(requestURL)  # , headers={"Authorization": "Bearer " + config["clash_api_key"]})
    if response.status_code == 200:
        #info = response.json()
        return True  #info["name"]
    else:
        return False


def get_clan_name(tag):
    requestURL = f"{config["clan_request_url"]}{tag}"
    response = requests.get(requestURL)
    info = response.json()
    return info["name"]