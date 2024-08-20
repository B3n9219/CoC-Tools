from settings import *
from player import *
import requests


def get_clan_members_json_info():
    requestURL = clanRequestURL + clanTag + "/members"
    response = requests.get(requestURL)#, headers={"Authorization": "Bearer " + apiKey})
    #print(response.json())
    clanMemberInfo = response.json()["items"]
    return clanMemberInfo


def convert_json_time_to_date(time):
    formated_date = f"{time[6:8]}/{time[4:6]}/{time[0:4]}"
    return formated_date

def find_last_filled_column(check_sheet):
    columnsFilled = sheet.read_range("1:1", check_sheet)
    column_title = columnsFilled[-1]
    column_index = column_to_number(len(columnsFilled))
    return column_index, column_title


def find_next_free_column(sheet_to_check):
    columns_filled = sheet.read_range("1:1",sheet_to_check)
    next_free_column = column_to_number(len(columns_filled)+1)
    return next_free_column


def prepare_attack_info_to_add(players_in_sheet, players_in_clan, player_attack_info, attack_type, no_info_value):
    attack_info_to_add = []
    for player in players_in_sheet:
        attack_info_found = False
        if player.is_player_in_list(players_in_clan):
            for item in player_attack_info:
                if player.is_player_equal_to(item):    #"[[name,tag][attacks,gold]]"
                    attack_info_to_add.append(item.get_attacks(attack_type))
                    attack_info_found = True
                    print(f"{player.name} used {item.get_attacks(attack_type)} attacks")
                    break
            if not attack_info_found:
                print(f"{player.name} did not attack")
                attack_info_to_add.append(no_info_value)
        else:
            attack_info_to_add.append("")
            print(f"{player.name} was not in the clan")
    return attack_info_to_add


def prepare_attack_column_title(attack_type, start_date, column_filled_count, update_sheet):
    column_index, column_title = find_last_filled_column(update_sheet)
    freeColumn = find_next_free_column(update_sheet)
    print("Filled column",column_index,"Free colum :",freeColumn)
    currentEntryNum = int(column_filled_count)
    entryTitle = f"{attack_type} {currentEntryNum} \n {start_date}"
    # print(f"raid title {entryTitle}  lastFilled weekend = {column_title}")
    if entryTitle == column_title:
        updateColumn = column_index
        # print("UPDATE",updateColumn)
    else:
        updateColumn = freeColumn
        # print("update",updateColumn)
        entryTitle = f"{attack_type} {currentEntryNum + 1} \n {start_date}"
    return entryTitle, updateColumn


def add_attack_info_to_sheet(attack_info_to_add, entry_title, update_column, updateSheet):
    print(attack_info_to_add)
    sheet.update_cell(f"{update_column}1", entry_title, updateSheet)
    sheet.batch_update_cells(
        f"{update_column}{sheetHeadingOffset}:{update_column}{len(attack_info_to_add) + sheetHeadingOffset}",
        attack_info_to_add, updateSheet)


def get_players_in_sheet():
    playerNames = sheet.read_range(entire_column(nameColumn),memberSheet)
    playerTags = sheet.read_range(entire_column(tagColumn),memberSheet)
    playerClanStatus = sheet.read_range(entire_column(clanStatusColumn),memberSheet)
    playerNum = max(len(playerNames),len(playerTags))
    players = []
    if len(playerNames) != len(playerTags):
        raise Exception("Not the same number or player names and tags in the spreadsheet")
    for i in range (0,playerNum):
        players.append(Player(name=playerNames[i], tag=playerTags[i], clan_status=playerClanStatus[i]))
    return players

def get_players_in_clan():
    jsonInfo = get_clan_members_json_info()
    members = []
    for playerJsonInfo in jsonInfo:
        player = Player(name=playerJsonInfo["name"], tag=playerJsonInfo["tag"], role=playerJsonInfo["role"],
                        th_level=playerJsonInfo["townHallLevel"], clan_status="TRUE")
        members.append(player)
    return members