import requests
from settings import *
import utilities as util
from player import *
import re

def get_ck_war_info():
    requestURL = f"{baseRequest}/war/%23{clanTag}/previous?limit=3"
    print(requestURL)
    response = requests.get(requestURL)
    info = response.json()
    war_statuses = {}
    for item in info:
        formatted_date = util.convert_json_time_to_date(item["startTime"])
        war_statuses[formatted_date] = item["state"]
    return info, war_statuses

def find_war_endpoint(war):
    if war["clan"]["tag"] == f"#{clanTag}":
        return "clan"
    else:
        return "opponent"


def check_war_status_validity(players_in_sheet, players_in_clan, war_info, api_war_statuses):
    print(api_war_statuses)
    sheet_war_titles = sheet.read_range("1:1", warSheet)
    sheet_war_statuses = sheet.read_range("2:2", warSheet)[war_info_columns:]
    pattern = r'\d{2}/\d{2}/\d{4}'
    sheet_war_dates = []
    for title in sheet_war_titles:
        match = re.search(pattern, title)
        if match:
            date = match.group()
            sheet_war_dates.append(date)
            #print("Extracted date:", date)
        else:
            pass
            #print(title,"no match")
    #print(sheet_war_dates, sheet_war_statuses)
    for i in range(0, len(sheet_war_dates)):
        if sheet_war_dates[i] in api_war_statuses:
            #print(sheet_war_statuses[i],api_war_statuses[sheet_war_dates[i]])
            if sheet_war_statuses[i] != api_war_statuses[sheet_war_dates[i]]:
                for war in war_info:
                    if util.convert_json_time_to_date(war["startTime"]) == sheet_war_dates[i]:
                        clan_endpoint = find_war_endpoint(war)
                        war_attack_info = filter_war_info(war[clan_endpoint]["members"])
                        update_column = i+1+war_info_columns
                        update_column = column_to_number(update_column)
                        #print(sheet_war_dates[i],filter_war_info(war["clan"]["members"]),i+1+war_info_columns)
                        title = sheet_war_titles[i+war_info_columns].split('\n')[0] + '\n'
                        title = f"{title}{sheet_war_dates[i]}"
                        print(war_attack_info)
                        add_war_to_sheet(players_in_sheet,players_in_clan,war_attack_info, update_column, title, api_war_statuses[sheet_war_dates[i]])





def get_recent_war_info():
    requestURL = clanRequestURL + clanTag + "/currentwar"
    response = requests.get(requestURL, headers={"Authorization": "Bearer " + apiKey})
    #print(response.json())
    info = response.json()
    startDate = info["startTime"]
    war_state = info["state"]
    #startDate = startDate[:8]  #removing the time from the startDate
    clanMemberInfo = info["clan"]["members"]
    formatted_date = util.convert_json_time_to_date(startDate)
    return formatted_date, war_state, filter_war_info(clanMemberInfo)

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
    util.add_attack_info_to_sheet(info_to_add, column_title, update_column, warSheet)
    sheet.update_cell(f"{update_column}2", f"status: {status}",warSheet)


def update_war_sheet():
    players_in_sheet = util.get_players_in_sheet()
    players_in_clan = util.get_players_in_clan()
    info, war_statuses = get_ck_war_info()
    check_war_status_validity(players_in_sheet,players_in_clan,info, war_statuses)
    add_new_war(players_in_sheet, players_in_clan)

def update_past_war():
    pass
def add_new_war(players_in_sheet, players_in_clan):
    start_date, war_state, player_war_info = get_recent_war_info()
    status = get_recent_war_status(start_date, war_state)
    column_title, update_column = util.prepare_attack_column_title("War", start_date, sheetSettings["normalWarsAdded"], warSheet)
    if war_state != 'preparation':
        add_war_to_sheet(players_in_sheet, players_in_clan, player_war_info, update_column, column_title, status)

def get_recent_war_status(start_date, war_state):
    war_start_date = datetime.strptime(start_date, '%d/%m/%Y')
    date_difference = abs((war_start_date - currentDate).days)
    within_two_days = date_difference <= 2
    if within_two_days:
        if war_state == "preparation":
            return "prep day"
        else:
            return "battle day"
    else:
        return "war ended"