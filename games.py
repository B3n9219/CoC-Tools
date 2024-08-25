import requests
from settings import *
import utilities as util
from player import *

def get_clan_games_json_info():
    players_in_clan = util.get_players_in_clan()
    json_info = []
    for player in players_in_clan:
        player_tag = player.tag[1:] #removing the '#' from the start of the tag
        requestURL = playerRequestURL + player_tag + "/stats"
        response = requests.get(requestURL)
        json_info.append(response.json())
    return json_info


def get_clan_games_info():
    currentDay = currentDate.day
    if int(currentDay) < 22:
        updateDate = currentDate - relativedelta(months=1)
    else:
        updateDate = currentDate
    update_date_str = str(updateDate)[:7]
    json_info = get_clan_games_json_info()
    clan_games_participants = []
    for player_info in json_info:
        player = Player(name=player_info["name"], tag=player_info["tag"])
        try:
            player.games_score = player_info["clan_games"][update_date_str]["points"]
            clan_games_participants.append(player)
        except:
            player.games_score = 0
            clan_games_participants.append(player)
    return update_date_str, clan_games_participants



def update_games_sheet():
    players_in_sheet = util.get_players_in_sheet()
    players_in_clan = util.get_players_in_clan()
    start_date, player_games_info = get_clan_games_info()
    print(start_date)
    info_to_add = util.prepare_attack_info_to_add(players_in_sheet, players_in_clan, player_games_info,"Games", 0)
    column_title, update_column = util.prepare_attack_column_title("Clan Games", start_date, sheetSettings["clanGamesAdded"], clanGamesSheet)
    util.add_attack_info_to_sheet(info_to_add, column_title, update_column, clanGamesSheet)
