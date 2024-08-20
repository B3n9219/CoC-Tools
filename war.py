from settings import *
import requests
import spreadsheet as sheet
from player import *
import utilities as util

def get_recent_war_info():
    requestURL = clanRequestURL + clanTag + "/currentwar"
    response = requests.get(requestURL, headers={"Authorization": "Bearer " + apiKey})
    #print(response.json())
    info = response.json()
    startDate = info["startTime"]
    startDate = startDate[:8]  #removing the time from the startDate
    clanMemberInfo = info["clan"]["members"]
    return startDate, clanMemberInfo

def filter_war_info():
    startDate, memberInfo = get_recent_war_info()
    formatedDate = util.convert_json_time_to_date(startDate)
    playerWarInfo = []
    for item in memberInfo:
        try:
            attacks_used = len(item["attacks"])
        except:
            attacks_used = 0
        player = Player(name=item["name"], tag=item["tag"], war_attacks=attacks_used)
        playerWarInfo.append(player)
    return formatedDate, playerWarInfo


def update_war_sheet():
    players_in_sheet = util.get_players_in_sheet()
    players_in_clan = util.get_players_in_clan()
    start_date, player_war_info = filter_war_info()
    info_to_add = util.prepare_attack_info_to_add(players_in_sheet, players_in_clan, player_war_info, "War","")
    column_title, update_column = util.prepare_attack_column_title("War", start_date, sheetSettings["normalWarsAdded"], warSheet)
    util.add_attack_info_to_sheet(info_to_add, column_title, update_column, warSheet)



