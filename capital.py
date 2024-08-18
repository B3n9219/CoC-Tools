from settings import *
import requests
import spreadsheet as sheet
import members
from player import *


def get_raid_weekend_info():
    requestURL = clanRequestURL + clanTag + "/capitalraidseasons"
    response = requests.get(requestURL, headers={"Authorization": "Bearer " + apiKey})
    #print(response.json())
    info = response.json()["items"][0]
    startDate = info["startTime"]
    startDate = startDate[:8]  #removing the time from the startDate
    clanMemberInfo = info["members"]
    return startDate, clanMemberInfo


def filter_info():
    startDate, memberInfo = get_raid_weekend_info()
    formatedDate = f"{startDate[6:8]}/{startDate[4:6]}/{startDate[0:4]}"
    playerRaidInfo = []
    for item in memberInfo:
        player = Player(name=item["name"], tag=item["tag"], raid_attacks=item["attacks"], gold_looted=item["capitalResourcesLooted"])
        playerRaidInfo.append(player)
    return formatedDate, playerRaidInfo


def update_capital():
    startDate, playerRaidInfo = filter_info()
    players_in_sheet = []
    playersInSheetNames = sheet.read_range(entire_column(nameColumn), capitalSheet)
    playersInSheetTags = sheet.read_range(entire_column(tagColumn),capitalSheet)
    for i in range (0,max(len(playersInSheetNames),len(playersInSheetTags))):
        players_in_sheet.append(Player(name=playersInSheetNames[i], tag=playersInSheetTags[i]))
    players_in_sheet = players_in_sheet[1:] #removing the title row from the list
    playersInClan = members.get_players_in_clan()
    add_raid_attacks_to_sheet(players_in_sheet, playersInClan, playerRaidInfo, startDate)
    '''
    for player in playerRaidInfo:
        if player[0] in players_in_sheet:
            playerSheetIndex = players_in_sheet.index(player[0])
            print(f"adding {player[1][0]["attacks"]} to row {playerSheetIndex}")
            sheet.update_cell(f"D{playerSheetIndex+sheetHeadingOffset}", player[1][0]["attacks"], capitalSheet)
    '''


def find_last_entered_weekend():
    columnsFilled = sheet.read_range("1:1", capitalSheet)
    weekendTitle = columnsFilled[-1]
    weekendColumnNum = column_to_number(len(columnsFilled))
    return weekendColumnNum, weekendTitle


def find_next_free_column():
    columnsFilled = sheet.read_range("1:1",capitalSheet)
    nextFreeColumn = column_to_number(len(columnsFilled)+1)
    return nextFreeColumn


def add_raid_attacks_to_sheet(playersInSheet, playersInClan, playerRaidInfo, startDate):
    raidInfoToAdd = []
    for player in playersInSheet:
        raidInfoFound = False
        if player.is_player_in_list(playersInClan):
            for item in playerRaidInfo:
                if player.is_player_equal_to(item):    #"[[name,tag][attacks,gold]]"
                    raidInfoToAdd.append(item.raid_attacks)
                    raidInfoFound = True
                    print(f"{player.name} used {item.raid_attacks} attacks")
                    break
            if not raidInfoFound:
                print(f"{player.name} did not attack")
                raidInfoToAdd.append(0)
        else:
            raidInfoToAdd.append("")
            print(f"{player.name} was not in the clan")
    lastFilledColumn, lastFilledWeekend = find_last_entered_weekend()
    freeColumn = find_next_free_column()
    currentWeekendNum = int(sheetSettings["raidWeekendsAdded"])
    raidWeekendTitle = f"Raid Weekend {currentWeekendNum} \n {startDate}"
    #print(f"raid title {raidWeekendTitle}  lastFilled weekend = {lastFilledWeekend}")
    if raidWeekendTitle == lastFilledWeekend:
        updateColumn = lastFilledColumn
        #print("UPDATE",updateColumn)
    else:
        updateColumn = freeColumn
        #print("update",updateColumn)
        raidWeekendTitle = f"Raid Weekend {currentWeekendNum+1} \n {startDate}"

    sheet.update_cell(f"{updateColumn}1",raidWeekendTitle,capitalSheet)
    sheet.batch_update_cells(f"{updateColumn}{1+sheetHeadingOffset}:{updateColumn}{len(raidInfoToAdd)+sheetHeadingOffset}",raidInfoToAdd,capitalSheet)





