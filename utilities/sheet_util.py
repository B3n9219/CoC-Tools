import requests
import json

from config.config import config
from utilities.general_util import entire_column, column_num_to_letter, strip_title
from discord_bot.spreadsheet.player import *
from discord_bot.spreadsheet import spreadsheet as sheet


def get_clan_members_json_info():
    # member data includes: name, tag, TH, role etc...
    requestURL = config["clan_request_url"] + config["clan_tag"] + "/members"
    response = requests.get(requestURL)
    clanMemberInfo = response.json()["items"]
    return clanMemberInfo


def convert_json_time_to_date(time):
    # json times are just a string of numbers, e.g. YYYYMMDD
    try:  # if time passed is convertable it will be
        # makes json time (YYYYMMDD) into more readable DD/MM/YYYY
        formated_date = f"{time[6:8]}/{time[4:6]}/{time[0:4]}"
    except:  # if time passed is not valid will return the time passed into the function
        formated_date = time
    return formated_date


def find_last_filled_column(check_sheet):
    # reading the first row of passed sheet
    columnsFilled = sheet.read_range("1:1", check_sheet)
    # column_title set to the title of the last filled column
    column_title = columnsFilled[-1]
    # column_index set to the index of the last filled column
    column_index = len(columnsFilled)
    return column_index, column_title


def find_next_free_column(sheet_to_check):
    """
    Finds the next free column in a given sheet
    :param sheet_to_check: e.g. WAR
    :return: next free column (letter, e.g. C)
    """
    columns_filled = sheet.read_range("1:1", sheet_to_check)
    next_free_column = column_num_to_letter(len(columns_filled) + 1)
    return next_free_column


def prepare_attack_info_to_add(players_in_sheet, players_in_clan, players_attack_info, attack_type, no_info_value):
    """
    Creates a list of attacks used / stars earned / CG medals
    :param players_in_sheet: list of player objects in a sheet.  Includes: name, tag, and clan status
    :param players_in_clan: list of player objects of ppl who are currently in the clan.
                            Includes: name, tag, role, TH and clan status (which is always TRUE)
    :param players_attack_info: list of player objects, including name, tag, and attack info (e.g. attacks used)
    :param attack_type: type of attack (e.g. war, raid, games)
    :param no_info_value: value used when player is in sheet + clan but has no attack info in players_attack_info
    :return: returns a list of attacks used by each member
    """
    attack_info_to_add = []
    for player_in_sheet in players_in_sheet:
        attack_info_found = False
        if player_in_sheet.is_player_in_list(players_in_clan):  # triggered if players in sheet AND in the clan
            for player_attack_info in players_attack_info:  # looping through the attacks used by each clan member
                # checking if the player in sheet's tag is the same as the player_attack_info tag
                if player_in_sheet.is_player_equal_to(player_attack_info):
                    # adding the number of attacks used to a list
                    attack_info_to_add.append(player_attack_info.get_attacks(attack_type))
                    attack_info_found = True
                    break
            if not attack_info_found:
                attack_info_to_add.append(no_info_value)  # no_info value is 0 for raid, wars, and CG, and "" for CWL
        else:
            attack_info_to_add.append("")  # appends "" when there is no data for the player
    return attack_info_to_add


def prepare_attack_column_title(attack_type, start_date, column_filled_count, update_sheet):
    """
    prepares the column title for an event. e.g:    Raid Weekend 3
                                                      29/07/2024
    :param attack_type: type of attack (e.g. war, raid, games)
    :param start_date: date event started - in format DD/MM/YYYY
    :param column_filled_count: number of events already added (e.g. 5 raid weekends)
    :param update_sheet: sheet to be updated
    :return: returns the title for the entry and the column that needs to be updated next
    """
    # finding the last filled column and converting it to letter / spreadsheet column.  e.g. 3 -> C
    last_column_index, last_column_title = find_last_filled_column(update_sheet)
    last_column_letter = column_num_to_letter(last_column_index)
    freeColumn = find_next_free_column(update_sheet)
    currentEntryNum = int(column_filled_count)
    entryTitle = f"{attack_type} {currentEntryNum} \n {start_date}"
    # checking if the entry being prepared is already in the spreadsheet

    if strip_title(entryTitle) == strip_title(last_column_title):
        # if it is update_column set to last entered column, so the data is overwritten / updated
        update_column = last_column_letter
    else:
        update_column = freeColumn
        entryTitle = f"{attack_type} {currentEntryNum + 1}\n{start_date}"
    return entryTitle, update_column


def add_attack_info_to_sheet(attack_info_to_add, entry_title, update_column, update_sheet, additional_offset=0):
    """
    adds the attack info previously prepared into the correct format into the desired sheet
    :param attack_info_to_add: list of attacks used in an event by each player in clan
    :param entry_title: column title of entry.  e.g. War 3 \n 12/05/23
    :param update_column: column that needs to be updated (letter e.g. C)
    :param update_sheet: sheet that needs to be updated e.g. WAR
    :param additional_offset: default set to 0.  For CWL set to 1
    :return: nothing
    """
    sheet.update_cell(f"{update_column}{1+additional_offset}", entry_title, update_sheet)
    sheet.batch_update_cells(
        f"{update_column}{config['title_row_offset']+1}:{update_column}{len(attack_info_to_add) + config['title_row_offset'] + additional_offset}",
        attack_info_to_add, update_sheet)


def get_players_in_sheet(check_sheet):
    playerNames = sheet.read_range(entire_column(config["name_column"]), check_sheet)
    playerTags = sheet.read_range(entire_column(config["tag_column"]), check_sheet)
    playerClanStatus = sheet.read_range(entire_column(config["clan_status_column"]), check_sheet)
    playerNum = max(len(playerNames),len(playerTags))
    players = []
    print("NAMES", playerNames)
    print("TAGS", playerTags)
    if len(playerNames) != len(playerTags):
        raise Exception("Not the same number or player names and tags in the spreadsheet")
    # turning the list of player attributes into an object
    for i in range(0, playerNum):
        players.append(Player(name=playerNames[i], tag=playerTags[i], clan_status=playerClanStatus[i]))
    return trim_players_in_sheet(players)


def trim_players_in_sheet(players):
    """
    trims the list of player objects into a list of player objects, where each player has a valid tag
    :param players: list of player objects
    :return: returns list of player objects where all players have valid tags
    """
    i = 0
    while players[i].tag[0] != "#":
        i += 1
    return players[i:]


def get_players_in_clan():
    jsonInfo = get_clan_members_json_info()
    members = []
    for playerJsonInfo in jsonInfo:
        player = Player(name=playerJsonInfo["name"], tag=playerJsonInfo["tag"], role=playerJsonInfo["role"],
                        th_level=playerJsonInfo["townHallLevel"], clan_status="TRUE")
        members.append(player)
    return members


def print_json(text):
    json_formatted_str = json.dumps(text, indent=2)
    print(json_formatted_str)