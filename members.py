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


def get_next_free_row(column,playersInSheet = None):
    if playersInSheet is None:
        playersInSheet = get_players_in_sheet()
    rowsOccupied = len(playersInSheet)
    print("next free row",rowsOccupied + sheetHeadingOffset)
    return rowsOccupied + sheetHeadingOffset


def update_spreadsheet_member_list():
    playersInClan = get_players_in_clan()
    playersInSheet = get_players_in_sheet()
    #playerInClanStatus = sheet.read_range(entire_column(clanStatusColumn),memberSheet)
    for player in playersInSheet:
        index = playersInSheet.index(player)
        #playerName = player[0] #0 is index for players name
        try:
            if player.is_player_in_list(playersInClan) and player.clan_status == "TRUE":
                # Do nothing
                pass
            elif player.is_player_in_list(playersInClan) and player.clan_status == "FALSE":
                print(f"{player} is in the clan but {player}'s status is set to 'FALSE'")
                # update status from FALSE to TRUE
                sheet.update_cell(clanStatusColumn + str(index + sheetHeadingOffset), "TRUE", memberSheet)
            elif not player.is_player_in_list(playersInClan) and player.clan_status == "TRUE":
                print(f"{player} is not in the clan but their status is set to 'TRUE'")
                # update status from TRUE to FALSE
                sheet.update_cell(clanStatusColumn + str(index + sheetHeadingOffset), "FALSE", memberSheet)
            elif not player.is_player_in_list(playersInClan) and player.clan_status == "FALSE":
                # Do nothing
                pass
        except:
            if player in playersInClan:
                print(f"{player} is in the clan but their in clan status is set to ' '")
            else:
                print(f"{player} is not in the clan but their in clan status is set to ' '")
    nextFreeRow = get_next_free_row(nameColumn, playersInSheet)
    for player in playersInClan:
        if not player.is_player_in_list(playersInSheet):
            print(f"{player} is in the clan, but not in the spreadsheet")
            playerInfo = [player.name,player.tag,player.role,player.th_level,player.clan_status]
            sheet.batch_update_cells(f"{nameColumn}{nextFreeRow}:{clanStatusColumn}{nextFreeRow}",playerInfo,memberSheet)
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
    sheet.batch_update_cells(f"{nameColumn}{1+sheetHeadingOffset}:{nameColumn}{len(name_update_list)+sheetHeadingOffset}",name_update_list,memberSheet)
    sheet.batch_update_cells(f"{tagColumn}{1+sheetHeadingOffset}:{tagColumn}{len(tag_update_list)+sheetHeadingOffset}",tag_update_list,memberSheet)
    sheet.batch_update_cells(f"{roleColumn}{1+sheetHeadingOffset}:{roleColumn}{len(role_update_list)+sheetHeadingOffset}",role_update_list,memberSheet)
    sheet.batch_update_cells(f"{THLevelColumn}{1+sheetHeadingOffset}:{THLevelColumn}{len(th_update_list)+sheetHeadingOffset}",th_update_list,memberSheet)
    sheet.batch_update_cells(f"{clanStatusColumn}{1+sheetHeadingOffset}:{clanStatusColumn}{len(status_update_list)+sheetHeadingOffset}",status_update_list,memberSheet)





