import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

from config.config import config
from utilities import sheet_util as util
from player.player import *


def get_clan_games_json_info():
    players_in_clan = util.get_players_in_clan()
    json_info = []
    for player in players_in_clan:
        player_tag = player.tag[1:] #removing the '#' from the start of the tag
        requestURL = config["player_request_url"] + player_tag + "/stats"
        response = requests.get(requestURL)
        if response.status_code == 200:
            json_info.append((response.json(),True))
        else:
            json_info.append(({"name": player.name, "tag": player.tag},False))
    return json_info


def get_clan_games_info():
    currentDate = datetime.now()
    currentDay = currentDate.day
    if int(currentDay) < 22:
        updateDate = currentDate - relativedelta(months=1)
    else:
        updateDate = currentDate
    update_date_str = str(updateDate)[:7]
    json_info = get_clan_games_json_info()
    clan_games_participants = []
    for player_info in json_info:
        player_stats = player_info[0]
        player = Player(name=player_stats["name"], tag=player_stats["tag"])
        try:
            player.games_score = player_stats["clan_games"][update_date_str]["points"]
            if player.games_score > 4000:
                player.games_score = 4000
            clan_games_participants.append(player)
        except:
            if player_info[1] == True:
                player.games_score = 0
            else:
                player.games_score = ""
            clan_games_participants.append(player)
    return update_date_str, clan_games_participants



def update_games_sheet():
    players_in_sheet = util.get_players_in_sheet(config["clan_games_sheet"])
    players_in_clan = util.get_players_in_clan()
    start_date, player_games_info = get_clan_games_info()
    info_to_add = util.prepare_attack_info_to_add(players_in_sheet, players_in_clan, player_games_info,"Games", 0)
    column_title, update_column = util.prepare_attack_column_title("Clan Games", start_date, config["clanGamesAdded"], config["clan_games_sheet"])
    util.add_attack_info_to_sheet(info_to_add, column_title, update_column, config["clan_games_sheet"])
