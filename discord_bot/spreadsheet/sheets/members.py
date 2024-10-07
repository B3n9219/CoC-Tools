import requests


from config.config import config
from utilities.general_util import entire_column
from discord_bot.spreadsheet.player import Player
from discord_bot.spreadsheet import spreadsheet as sheet


def get_clan_members_json_info():
    requestURL = config["clan_request_url"] + config["clan_tag"] + "/members"
    response = requests.get(requestURL, headers={"Authorization": "Bearer " + config["clash_api_key"]})
    if "items" in response.json():
        clanMemberInfo = response.json()["items"]
    else:
        print(f"request URL: {requestURL}, status code: {response.status_code}, json: {response.json()}")
        clanMemberInfo = None

    return clanMemberInfo


def get_players_in_clan():
    jsonInfo = get_clan_members_json_info()
    members = []
    for playerJsonInfo in jsonInfo:
        player = Player(name=playerJsonInfo["name"], tag=playerJsonInfo["tag"], role=playerJsonInfo["role"],
                        th_level=playerJsonInfo["townHallLevel"], clan_status="TRUE")
        members.append(player)
    return members


def get_players_in_sheet():
    playerNames = sheet.read_range(entire_column(config["name_column"]), config["member_sheet"])
    playerTags = sheet.read_range(entire_column(config["tag_column"]),config["member_sheet"])
    playerClanStatus = sheet.read_range(entire_column(config["clan_status_column"]),config["member_sheet"])
    playerNum = max(len(playerNames),len(playerTags))
    players = []
    if len(playerNames) != len(playerTags):
        raise Exception("Not the same number or player names and tags in the spreadsheet")
    for i in range (0,playerNum):
        players.append(Player(name=playerNames[i], tag=playerTags[i], clan_status=playerClanStatus[i]))
    return players


def get_next_free_row(column, playersInSheet = None):
    if playersInSheet is None:
        playersInSheet = get_players_in_sheet()
    rows_occupied = len(playersInSheet)
    next_free_row = rows_occupied + config["title_row_offset"] + 1
    return next_free_row


def add_new_members_to_sheet(players_in_clan,players_in_sheet):
    nextFreeRow = get_next_free_row(config["name_column"], players_in_sheet)
    for player in players_in_clan:
        if not player.is_player_in_list(players_in_sheet):
            print(f"{player} is in the clan, but not in the spreadsheet")
            playerInfo = [player.name, player.tag, player.clan_status, player.role, player.th_level]
            print("NEXT ROW", nextFreeRow)
            sheet.batch_update_cells(f"{config['name_column']}{nextFreeRow}:{config['th_level_column']}{nextFreeRow}",playerInfo,config['member_sheet'])
            nextFreeRow += 1


def update_member_sheet():
    players_in_clan = get_players_in_clan()
    players_in_sheet = get_players_in_sheet()
    players_in_sheet = players_in_sheet[1:]
    players_in_sheet_roles = sheet.read_range(entire_column(config["role_column"]),config["member_sheet"])
    players_in_sheet_th_levels = sheet.read_range(entire_column(config["th_level_column"]),config["member_sheet"])
    player_info = []
    clan_member_map = {player.tag: player for player in players_in_clan}
    for player in players_in_sheet:
        if player.tag in clan_member_map:
            clan_member = clan_member_map[player.tag]
            player_info.append([clan_member.name, clan_member.tag, clan_member.role,
                                clan_member.th_level, clan_member.clan_status])
        else:
            playerIndex = players_in_sheet.index(player)
            player_info.append([player.name, player.tag, players_in_sheet_roles[playerIndex],
                                players_in_sheet_th_levels[playerIndex],"FALSE"])
    name_update_list, tag_update_list, role_update_list, th_update_list, status_update_list = ([]for _ in range(5))
    for item in player_info:
        name_update_list.append(item[0])
        tag_update_list.append(item[1])
        role_update_list.append(item[2])
        th_update_list.append(item[3])
        status_update_list.append(item[4])
    sheet.batch_update_cells(f'{config["name_column"]}{1 + config["title_row_offset"]}:{config["name_column"]}{len(name_update_list) + config["title_row_offset"]}', name_update_list, config["member_sheet"])
    sheet.batch_update_cells(f'{config["tag_column"]}{1 + config["title_row_offset"]}:{config["tag_column"]}{len(tag_update_list) + config["title_row_offset"]}', tag_update_list, config["member_sheet"])
    sheet.batch_update_cells(f'{config["role_column"]}{1 + config["title_row_offset"]}:{config["role_column"]}{len(role_update_list) + config["title_row_offset"]}', role_update_list, config["member_sheet"])
    sheet.batch_update_cells(f'{config["th_level_column"]}{1 + config["title_row_offset"]}:{config["th_level_column"]}{len(th_update_list) + config["title_row_offset"]}', th_update_list, config["member_sheet"])
    sheet.batch_update_cells(f'{config["clan_status_column"]}{1 + config["title_row_offset"]}:{config["clan_status_column"]}{len(status_update_list) + config["title_row_offset"]}', status_update_list, config["member_sheet"])
    add_new_members_to_sheet(players_in_clan, players_in_sheet)