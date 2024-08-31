from settings import *
from player import *
import requests
import spreadsheet as sheet


def get_clan_members_json_info():
    requestURL = clanRequestURL + clanTag + "/members"
    response = requests.get(requestURL, headers={"Authorization": "Bearer " + apiKey})
    #print(response.json())
    clanMemberInfo = response.json()["items"]
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


def get_next_free_row(column, playersInSheet = None):
    if playersInSheet is None:
        playersInSheet = get_players_in_sheet()
    rows_occupied = len(playersInSheet)
    next_free_row = rows_occupied + title_row_offset + 1
    print("next free row", next_free_row)
    return next_free_row


def add_new_members_to_sheet(players_in_clan,players_in_sheet):
    nextFreeRow = get_next_free_row(nameColumn, players_in_sheet)
    for player in players_in_clan:
        if not player.is_player_in_list(players_in_sheet):
            print(f"{player} is in the clan, but not in the spreadsheet")
            playerInfo = [player.name, player.tag, player.clan_status, player.role, player.th_level]
            sheet.batch_update_cells(f"{nameColumn}{nextFreeRow}:{THLevelColumn}{nextFreeRow}",playerInfo,memberSheet)
            nextFreeRow += 1


def update_member_sheet():
    players_in_clan = get_players_in_clan()
    players_in_sheet = get_players_in_sheet()
    players_in_sheet = players_in_sheet[1:]
    players_in_sheet_roles = sheet.read_range(entire_column(roleColumn),memberSheet)
    players_in_sheet_th_levels = sheet.read_range(entire_column(THLevelColumn),memberSheet)
    player_info = []
    clan_member_map = {player.tag: player for player in players_in_clan}
    for player in players_in_sheet:
        if player.tag in clan_member_map:
            clan_member = clan_member_map[player.tag]
            player_info.append([clan_member.name, clan_member.tag, clan_member.role,
                                clan_member.th_level, clan_member.clan_status])
        else:
            playerIndex = players_in_sheet.index(player)
            player_info.append([player.name,player.tag,players_in_sheet_roles[playerIndex],
                                players_in_sheet_th_levels[playerIndex],"FALSE"])
    name_update_list,tag_update_list,role_update_list,th_update_list, status_update_list = ([]for _ in range(5))
    for item in player_info:
        name_update_list.append(item[0])
        tag_update_list.append(item[1])
        role_update_list.append(item[2])
        th_update_list.append(item[3])
        status_update_list.append(item[4])
    sheet.batch_update_cells(f"{nameColumn}{1 + title_row_offset}:{nameColumn}{len(name_update_list) + title_row_offset}", name_update_list, memberSheet)
    sheet.batch_update_cells(f"{tagColumn}{1 + title_row_offset}:{tagColumn}{len(tag_update_list) + title_row_offset}", tag_update_list, memberSheet)
    sheet.batch_update_cells(f"{roleColumn}{1 + title_row_offset}:{roleColumn}{len(role_update_list) + title_row_offset}", role_update_list, memberSheet)
    sheet.batch_update_cells(f"{THLevelColumn}{1 + title_row_offset}:{THLevelColumn}{len(th_update_list) + title_row_offset}", th_update_list, memberSheet)
    sheet.batch_update_cells(f"{clanStatusColumn}{1 + title_row_offset}:{clanStatusColumn}{len(status_update_list) + title_row_offset}", status_update_list, memberSheet)
    add_new_members_to_sheet(players_in_clan, players_in_sheet)





