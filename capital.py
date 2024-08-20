from settings import *
import requests
import members
from player import *
import utilities as util


def get_raid_weekend_info():
    requestURL = clanRequestURL + clanTag + "/capitalraidseasons"
    response = requests.get(requestURL, headers={"Authorization": "Bearer " + apiKey})
    #print(response.json())
    info = response.json()["items"][0]
    startDate = info["startTime"]
    startDate = startDate[:8]  #removing the time from the startDate
    clanMemberInfo = info["members"]
    return startDate, clanMemberInfo


def filter_raid_info():
    startDate, memberInfo = get_raid_weekend_info()
    formatedDate = util.convert_json_time_to_date(startDate)
    playerRaidInfo = []
    for item in memberInfo:
        player = Player(name=item["name"], tag=item["tag"], raid_attacks=item["attacks"], gold_looted=item["capitalResourcesLooted"])
        playerRaidInfo.append(player)
    return formatedDate, playerRaidInfo

def update_raid_sheet():
    players_in_sheet = util.get_players_in_sheet()
    players_in_clan = util.get_players_in_clan()
    start_date, player_raid_info = filter_raid_info()
    info_to_add = util.prepare_attack_info_to_add(players_in_sheet, players_in_clan, player_raid_info,"Raid", 0)
    column_title, update_column = util.prepare_attack_column_title("Raid Weekend", start_date, sheetSettings["raidWeekendsAdded"], capitalSheet)
    util.add_attack_info_to_sheet(info_to_add, column_title, update_column, capitalSheet)




