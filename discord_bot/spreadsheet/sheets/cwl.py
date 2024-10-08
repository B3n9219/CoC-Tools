import requests
from datetime import datetime

from config.config import config
from utilities import sheet_util as util
from utilities.general_util import column_num_to_letter
from discord_bot.spreadsheet.player import Player
from discord_bot.spreadsheet import spreadsheet as sheet


def get_CWL_info():
    currentDate = datetime.now()
    start_date = str(currentDate)[:7]
    requestURL = f"{config['base_request_url']}/cwl/%23{config['clan_tag']}/{start_date}"
    response = requests.get(requestURL)
    if response.status_code == 200:
        info = response.json()["rounds"]
        player_attack_info = {}
        player_list = []
        for round in info:
            roundNum = info.index(round) + 1
            clan_info = []
            for clan in round["warTags"]:
                if clan["clan"]["tag"] == f"#{config['clan_tag']}":
                    #print("1ST", clan["startTime"][:8], clan["clan"]["name"])
                    clan_info.append(clan["clan"]["members"])
                elif clan["opponent"]["tag"] == f"#{config['clan_tag']}":
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
            player = Player(tag=info[0],name=info[1][0],cwl_stars=info[1][1], cwl_attacks_used=info[1][2], cwl_attacks_available=info[1][3])
            player_list.append(player)
        return start_date, player_list, True
    else:
        return "", [], False


def select_cwl_update_column(start_date):
    cwl_added_to_sheet = int(config["cwlSeasonsAdded"])
    last_cwl_index, last_cwl_title = util.find_last_filled_column(config["cwl_sheet"])
    next_free_column = cwl_added_to_sheet*config["columns_per_cwl"] + config["cwl_info_columns"] + 1
    entry_title = f"CWL {cwl_added_to_sheet} \n {start_date}"
    if entry_title == last_cwl_title:
        update_column = last_cwl_index
    else:
        update_column = next_free_column
        entry_title = f"CWL {cwl_added_to_sheet+1} \n {start_date}"
    return entry_title, update_column


def update_cwl_sheet():
    players_in_sheet = util.get_players_in_sheet(config["cwl_sheet"])
    players_in_clan = util.get_players_in_clan()
    start_date, player_cwl_info, info_found = get_CWL_info()
    print(player_cwl_info)
    if info_found:
        entry_title, update_column = select_cwl_update_column(start_date)

        sheet.merge_cells(0,1,update_column-1,update_column -1 + config["columns_per_cwl"],config["cwl_sheet"])
        sheet.update_cell(f"{column_num_to_letter(update_column)}1", entry_title, config["cwl_sheet"])

        info_to_add = util.prepare_attack_info_to_add(players_in_sheet, players_in_clan, player_cwl_info, "Stars", "")
        util.add_attack_info_to_sheet(info_to_add, "Stars Earned", column_num_to_letter(update_column), config["cwl_sheet"], 1)

        info_to_add = util.prepare_attack_info_to_add(players_in_sheet, players_in_clan, player_cwl_info, "AttacksUsed", "")
        util.add_attack_info_to_sheet(info_to_add, "Attacks Used", column_num_to_letter(update_column + 1), config["cwl_sheet"], 1)

        info_to_add = util.prepare_attack_info_to_add(players_in_sheet, players_in_clan, player_cwl_info, "AttacksAvailable", "")
        util.add_attack_info_to_sheet(info_to_add, "Attacks Available", column_num_to_letter(update_column + 2), config["cwl_sheet"], 1)

        sheet.update_cell(f"{column_num_to_letter(update_column + 3)}2", "Stars per Attack", config["cwl_sheet"])
        sheet.update_cell(f"{column_num_to_letter(update_column + 4)}2", "Attacks Missed", config["cwl_sheet"])