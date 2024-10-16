import requests

from config.config import config
from utilities import sheet_util as util
from player import *
from discord_bot.spreadsheet import spreadsheet as sheet


def get_raid_weekend_info():
    # returns a list of recent raid weekends for a clan.  But only the most recent one includes player attack data
    requestURL = config["clan_request_url"] + config["clan_tag"] + "/capitalraidseasons"
    response = requests.get(requestURL)
    items = response.json()["items"]
    if len(items) == 0:
        return None
    # only the first raid weekend included in the response has attack data so filtering out the rest of it
    info = items[0]
    raid_state = info["state"]
    startDate = info["startTime"]
    startDate = startDate[:8]  #removing the time from the startDate
    clanMemberInfo = info["members"]
    return startDate, raid_state, clanMemberInfo


def filter_raid_info():
    raid_info = get_raid_weekend_info()
    # checking if api returned no data for the current raid weekend
    if raid_info is None:
        return None
    start_date, raid_state, memberInfo = raid_info
    formated_date = util.convert_json_time_to_date(start_date)
    player_raid_info = []
    # creating a list of player objects including the num of attacks used as an attribute of the object.
    for item in memberInfo:
        player = Player(name=item["name"], tag=item["tag"], raid_attacks=item["attacks"],
                        gold_looted=item["capitalResourcesLooted"]) #don't actually use gold looted yet
        player_raid_info.append(player)
    return formated_date, raid_state, player_raid_info


def update_raid_sheet():
    players_in_sheet = util.get_players_in_sheet(config["raid_sheet"])
    players_in_clan = util.get_players_in_clan()
    raid_info = filter_raid_info()
    # checking if no raid weekend data was returned by the API
    if raid_info is None:
        return None
    start_date, api_raid_state, player_raid_info = raid_info
    info_to_add = util.prepare_attack_info_to_add(players_in_sheet, players_in_clan, player_raid_info,"Raid", 0)
    # attack column title includes: Raid Weekend, iteration of raid weekend (i.e 1 more than last) and start date
    column_title, update_column = util.prepare_attack_column_title("Raid Weekend", start_date, config['raidWeekendsAdded'], config['raid_sheet'])
    try:  # getting raid weekend statuses from sheet
        sheet_raid_state = sheet.read_range(f"{update_column}2", config['raid_sheet'])[0].split(":")[1].strip()
    except:  # exception if no statuses in range
        sheet_raid_state = "no status in sheet"
    if sheet_raid_state != "ended":  # i.e raid weekend is ongoing, so needs data refreshing
        # adding new attack data to sheet
        util.add_attack_info_to_sheet(info_to_add, column_title, update_column, config["raid_sheet"])
        # updating the raid weekend status to be correct
        sheet.update_cell(f"{update_column}2", f"status: {api_raid_state}", config['raid_sheet'])







