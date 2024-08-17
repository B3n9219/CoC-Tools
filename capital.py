from settings import *
import requests
import spreadsheet as sheet
import members


def get__raid_weekend_info():
    requestURL = clanRequestURL + clanTag + "/capitalraidseasons"
    response = requests.get(requestURL, headers={"Authorization": "Bearer " + apiKey})
    #print(response.json())
    info = response.json()["items"][0]
    startDate = info["startTime"]
    startDate = startDate[:8]  #removing the time from the startDate
    clanMemberInfo = info["members"]
    return startDate, clanMemberInfo


def filter_info():
    startDate, memberInfo = get__raid_weekend_info()
    formatedDate = f"{startDate[6:8]}/{startDate[4:6]}/{startDate[0:4]}"
    playerRaidInfo = []
    for item in memberInfo:
        player = [item["name"], item["tag"]]
        raidInfo = [{"attacks": item["attacks"],"capitalGoldLooted": item["capitalResourcesLooted"]}]
        playerRaidInfo.append([player,raidInfo])
    return formatedDate, playerRaidInfo


def update_capital():
    startDate, playerRaidInfo = filter_info()
    playerInfo = []
    playersInSheet = sheet.read_range(entire_column(nameColumn), capitalSheet)
    playersInSheetTags = sheet.read_range(entire_column(tagColumn),capitalSheet)
    for i in range (0,max(len(playersInSheet),len(playersInSheetTags))):
        playerInfo.append([playersInSheet[i],playersInSheetTags[i]])
    playerInfo = playerInfo[1:] #removing the title row from the list
    playersInClan = members.get_players_in_clan()
    add_raid_attacks_to_sheet(playerInfo, playersInClan, playerRaidInfo, startDate)
    '''
    for player in playerRaidInfo:
        if player[0] in playerInfo:
            playerSheetIndex = playerInfo.index(player[0])
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
        if player in playersInClan:
            for item in playerRaidInfo:
                if player == item[0]:
                    raidInfoToAdd.append(item[1][0]["attacks"])
                    raidInfoFound = True
                    print(f"{player} used {item[1][0]["attacks"]} attacks")
                    break
            if not raidInfoFound:
                print(f"{player} did not attack")
                raidInfoToAdd.append(0)
        else:
            raidInfoToAdd.append("")
            print(f"{player} was not in the clan")
    lastFilledColumn, lastFilledWeekend = find_last_entered_weekend()
    freeColumn = find_next_free_column()
    currentWeekendNum = int(sheetSettings["raidWeekendsAdded"])
    raidWeekendTitle = f"Raid Weekend {currentWeekendNum} \n {startDate}"
    print(f"raid title {raidWeekendTitle}  lastFilled weekend = {lastFilledWeekend}")
    if raidWeekendTitle == lastFilledWeekend:
        updateColumn = lastFilledColumn
        print("UPDATE",updateColumn)
    else:
        updateColumn = freeColumn
        print("update",updateColumn)
        raidWeekendTitle = f"Raid Weekend {currentWeekendNum+1} \n {startDate}"

    sheet.update_cell(f"{updateColumn}1",raidWeekendTitle,capitalSheet)
    sheet.batch_update_cells(f"{updateColumn}{1+sheetHeadingOffset}:{updateColumn}{len(raidInfoToAdd)+sheetHeadingOffset}",raidInfoToAdd,capitalSheet)





