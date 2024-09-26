import requests

from config.config import config
from utilities import sheet_util as util
from discord_bot.spreadsheet.player import *
from discord_bot.spreadsheet import spreadsheet as sheet



def get_raid_weekend_info():
    requestURL = config["clan_request_url"] + config["clan_tag"] + "/capitalraidseasons"
    response = requests.get(requestURL)
    info = response.json()["items"][0]
    raid_state = info["state"]
    startDate = info["startTime"]
    startDate = startDate[:8]  #removing the time from the startDate
    clanMemberInfo = info["members"]
    return startDate, raid_state, clanMemberInfo


def filter_raid_info():
    startDate, raid_state, memberInfo = get_raid_weekend_info()
    formatedDate = util.convert_json_time_to_date(startDate)
    playerRaidInfo = []
    for item in memberInfo:
        player = Player(name=item["name"], tag=item["tag"], raid_attacks=item["attacks"], gold_looted=item["capitalResourcesLooted"])
        playerRaidInfo.append(player)
    return formatedDate, raid_state,playerRaidInfo

def update_raid_sheet():
    players_in_sheet = util.get_players_in_sheet(config["raid_sheet"])
    players_in_clan = util.get_players_in_clan()
    start_date, api_raid_state, player_raid_info = filter_raid_info()
    info_to_add = util.prepare_attack_info_to_add(players_in_sheet, players_in_clan, player_raid_info,"Raid", 0)
    column_title, update_column = util.prepare_attack_column_title("Raid Weekend", start_date, config["raidWeekendsAdded"], config["raid_sheet"])
    try:
        sheet_raid_state = sheet.read_range(f"{update_column}2", config["raid_sheet"])[0].split(":")[1].strip()
    except:
        sheet_raid_state = "no status in sheet"
    if sheet_raid_state != "ended":
        util.add_attack_info_to_sheet(info_to_add, column_title, update_column, config["raid_sheet"])
        sheet.update_cell(f"{update_column}2", f"status: {api_raid_state}", config["raid_sheet"])







