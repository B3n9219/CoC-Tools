import re
import requests

from config.config import config
from utilities.general_util import column_to_number
from utilities import sheet_util as util
from discord_bot.spreadsheet.player import *
from discord_bot.spreadsheet import spreadsheet as sheet





def get_ck_war_info():
    requestURL = f"{config['base_request_url']}/war/%23{config['clan_tag']}/previous?limit=3"
    response = requests.get(requestURL)
    info = response.json()
    war_statuses = {}
    for item in info:
        formatted_date = util.convert_json_time_to_date(item["startTime"])
        war_statuses[formatted_date] = item["state"]
    return info, war_statuses

def find_war_endpoint(war):
    if war["clan"]["tag"] == f"#{config['clan_tag']}":
        return "clan"
    else:
        return "opponent"


def check_war_status_validity(players_in_sheet, players_in_clan, war_info, api_war_statuses):
    sheet_war_titles = sheet.read_range("1:1", config["war_sheet"])
    sheet_war_statuses = sheet.read_range("2:2", config["war_sheet"])[config["war_info_columns"]:]
    pattern = r'\d{2}/\d{2}/\d{4}'
    sheet_war_dates = []
    for title in sheet_war_titles:
        match = re.search(pattern, title)
        if match:
            date = match.group()
            sheet_war_dates.append(date)
        else:
            pass
    for i in range(0, len(sheet_war_dates)):
        if sheet_war_dates[i] in api_war_statuses:
            if sheet_war_statuses[i] != api_war_statuses[sheet_war_dates[i]]:
                for war in war_info:
                    if util.convert_json_time_to_date(war["startTime"]) == sheet_war_dates[i]:
                        clan_endpoint = find_war_endpoint(war)
                        war_attack_info = filter_war_info(war[clan_endpoint]["members"])
                        update_column = i+1+config["war_info_columns"]
                        update_column = column_to_number(update_column)
                        title = sheet_war_titles[i+config["war_info_columns"]].split('\n')[0] + '\n'
                        title = f"{title}{sheet_war_dates[i]}"
                        add_war_to_sheet(players_in_sheet,players_in_clan,war_attack_info, update_column, title, api_war_statuses[sheet_war_dates[i]])





def get_recent_war_info():
    requestURL = config["clan_request_url"] + config["clan_tag"] + "/currentwar"
    response = requests.get(requestURL, headers={"Authorization": "Bearer " + config["clash_api_key"]})
    info = response.json()
    if response.status_code == 200:
        war_state = info["state"]
        if war_state != "notInWar":
            startDate = info["startTime"]
            clanMemberInfo = info["clan"]["members"]
            formatted_date = util.convert_json_time_to_date(startDate)
            return formatted_date, war_state, filter_war_info(clanMemberInfo), True
        else:
            return "",war_state, [], True
    else:
        return "", "", [], False

def filter_war_info(memberInfo):
    playerWarInfo = []
    for item in memberInfo:
        try:
            attacks_used = len(item["attacks"])
        except:
            attacks_used = 0
        player = Player(name=item["name"], tag=item["tag"], war_attacks=attacks_used)
        playerWarInfo.append(player)
    return playerWarInfo


def add_war_to_sheet(players_in_sheet, players_in_clan, war_info, update_column, column_title, status):
    info_to_add = util.prepare_attack_info_to_add(players_in_sheet, players_in_clan, war_info, "War","")
    util.add_attack_info_to_sheet(info_to_add, column_title, update_column, config["war_sheet"])
    sheet.update_cell(f"{update_column}2", f"status: {status}",config['war_sheet'])


def update_war_sheet():
    players_in_sheet = util.get_players_in_sheet(config["war_sheet"])
    players_in_clan = util.get_players_in_clan()
    info, war_statuses = get_ck_war_info()
    check_war_status_validity(players_in_sheet,players_in_clan,info, war_statuses)
    add_new_war(players_in_sheet, players_in_clan)

def update_past_war():
    pass
def add_new_war(players_in_sheet, players_in_clan):
    start_date, war_state, player_war_info, found_status = get_recent_war_info()
    if found_status == True:
        if war_state != "notInWar":
            status = get_war_status_title(war_state)
            column_title, update_column = util.prepare_attack_column_title("War", start_date, config["normalWarsAdded"], config["war_sheet"])
            if war_state != 'preparation':
                add_war_to_sheet(players_in_sheet, players_in_clan, player_war_info, update_column, column_title, status)
            else:
                sheet.update_cell(f"{update_column}1", column_title, config['war_sheet'])
                sheet.update_cell(f"{update_column}2", f"status: {status}", config['war_sheet'])

def get_war_status_title(war_state):
    if war_state == "preparation":
        return "prep day"
    elif war_state == "inWar":
        return "battle day"
    else:
        return "war ended"