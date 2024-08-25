import requests
import json
from settings import *
import utilities as util
from player import *

def get_CWL_info():
    start_date = str(currentDate)[:7]
    requestURL = f"{baseRequest}/cwl/%23{clanTag}/{start_date}"
    response = requests.get(requestURL)#, headers={"Authorization": "Bearer " + apiKey})
    info = response.json()["rounds"]
    player_attack_info = {}
    player_list = []
    for round in info:
        roundNum = info.index(round) + 1
        clan_info = []
        #util.print_json(item_path)
        for clan in round["warTags"]:
            if clan["clan"]["tag"] == f"#{clanTag}":
                #print("1ST", clan["startTime"][:8], clan["clan"]["name"])
                clan_info.append(clan["clan"]["members"])
            elif clan["opponent"]["tag"] == f"#{clanTag}":
                #print("2ND", clan["startTime"][:8], clan["opponent"]["name"])
                clan_info.append(clan["opponent"]["members"])
        for attack_info in clan_info:
            for player_info in attack_info:
                stars_earned = 0
                attacks_used = 0
                attacks_available = 1
                player_tag = player_info["tag"]
                try:
                    stars_earned = player_info["attacks"][0]["stars"]
                    attacks_used = 1
                except:
                    stars_earned = 0
                    attacks_used = 0
                if player_tag in player_attack_info:
                    player_attack_info[player_tag][0] = player_info["name"]
                    player_attack_info[player_tag][1] += stars_earned
                    player_attack_info[player_tag][2] += attacks_used
                    player_attack_info[player_tag][3] += attacks_available
                else:
                    player_attack_info[player_info["tag"]] = [player_info["name"], stars_earned, attacks_used,
                                                              attacks_available]
    for info in list(player_attack_info.items()):
        print(info)
        player = Player(tag=info[0],name=info[1][0],cwl_stars=info[1][1], cwl_attacks_used=info[1][2], cwl_attacks_available=info[1][3])
        #print(f"name:{player.name} tag:{player.tag} cwl_stars:{player.cwl_stars} cwl_attacks_used{player.cwl_attacks_used} avaialable:{player.cwl_attacks_available}")
        player_list.append(player)
    return start_date, player_list


def find_last_filled_column(check_sheet):
    columnsFilled = sheet.read_range("1:1", check_sheet)
    column_title = columnsFilled[-1]
    column_index = column_to_number(len(columnsFilled))
    return column_index, column_title



def find_next_free_cwl_column():
    columns_filled = sheet.read_range("2:2", cwlSheet)
    if len(columns_filled) == 0:
        next_free_column = column_to_number(len(columns_filled)+1+3)
    else:
        next_free_column = column_to_number(len(columns_filled)+1)
    return next_free_column

def select_cwl_update_column(start_date):
    cwl_added_to_sheet = int(sheetSettings["cwlSeasonsAdded"])
    last_cwl_index, last_cwl_title = util.find_last_filled_column(cwlSheet)
    next_free_column = cwl_added_to_sheet*columns_per_CWL + CWL_info_columns + 1
    entry_title = f"CWL {cwl_added_to_sheet} \n {start_date}"
    if entry_title == last_cwl_title:
        update_column = last_cwl_index
    else:
        update_column = next_free_column
        entry_title = f"CWL {cwl_added_to_sheet+1} \n {start_date}"
    return entry_title, update_column






def update_cwl_sheet():
    players_in_sheet = util.get_players_in_sheet()
    players_in_clan = util.get_players_in_clan()
    start_date, player_cwl_info = get_CWL_info()

    entry_title, update_column = select_cwl_update_column(start_date)

    #cwl_column_index = int(sheetSettings["cwlSeasonsAdded"])*columns_per_CWL + CWL_info_columns + 1
    #print("CWL",cwl_column_index)
    #cwl_column = column_to_number(cwl_column_index)
    sheet.merge_cells(0,1,update_column-1,update_column -1 + columns_per_CWL,cwlSheet)
    sheet.update_cell(f"{column_to_number(update_column)}1", entry_title ,cwlSheet)

    info_to_add = util.prepare_attack_info_to_add(players_in_sheet, players_in_clan, player_cwl_info, "Stars", "")
    util.add_attack_info_to_sheet(info_to_add, "Stars Earned", column_to_number(update_column), cwlSheet, 1)

    info_to_add = util.prepare_attack_info_to_add(players_in_sheet, players_in_clan, player_cwl_info, "AttacksUsed", "")
    util.add_attack_info_to_sheet(info_to_add, "Attacks Used", column_to_number(update_column+1), cwlSheet, 1)

    info_to_add = util.prepare_attack_info_to_add(players_in_sheet, players_in_clan, player_cwl_info, "AttacksAvailable", "")
    util.add_attack_info_to_sheet(info_to_add, "Attacks Available", column_to_number(update_column+2), cwlSheet, 1)



