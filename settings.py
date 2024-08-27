import spreadsheet as sheet
from datetime import *
from dateutil.relativedelta import relativedelta

currentDate = datetime.now()

apiKey = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjZhZDAyZTc1LWIzMjctNGM3Yi1iNzljLWJiOTNkMzY4MWYyMyIsImlhdCI6MTcyMzMwMjMzMiwic3ViIjoiZGV2ZWxvcGVyL2E1Yjc0NTA2LWI3ZDQtZmE3OC0yMmU1LTMwYTg3OTM3YzBlYiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE0Ny4xNDcuOTIuNDMiXSwidHlwZSI6ImNsaWVudCJ9XX0.tObIRu64OrHg2tVMB6Ry4SPBGWQIvsRJNto3Z_9IO8V0pUMGgJoXRgLQl6phL_4sGGyVfYVpclo0Dre3e438YA"
baseRequest = "https://api.clashking.xyz"
playerRequestURL = f"{baseRequest}/player/%23"  #followed by player tag (no #)
clanRequestURL = f"{baseRequest}/v1/clans/%23"  #followed by clan tag (no #)


clanTag = "2R989CY89"
#clanTag = "2RLQPCVO8"
SPREADSHEET_ID = "1mnlquv54_uJrtR_FXwLlZhiM9lskqSwSbP-pBW2uN6A"
#SPREADSHEET_ID = "1FKPLEb4zvICDhsT0TgT8BlpWObj3kAR0y01W7RuuNUw"

columns_per_CWL = 3
CWL_info_columns = 3
war_info_columns = 6

sheetHeadingOffset = 2

#SPREADSHEET SHEET NAMES
memberSheet = "MEMBERS"
capitalSheet = "RAIDS"
settingsSheet = "SETTINGS"
warSheet = "WAR"
clanGamesSheet = "CLAN GAMES"
cwlSheet = "CWL"

#SPREADSHEET COLUMNS
nameColumn = "A"
tagColumn = "B"
roleColumn = "C"
THLevelColumn = "D"
clanStatusColumn = "E"

settingNameColumn = "A"
settingValueColumn = "B"

#Settings updated by spreadsheet
sheetSettings = {}
raidWeekendsAdded = []


def update_settings():
    global raidWeekendsAdded
    settingNames = sheet.read_range(entire_column(settingNameColumn),settingsSheet)
    settingValues = sheet.read_range(entire_column(settingValueColumn), settingsSheet)
    for i in range (0,len(settingNames)):
        sheetSettings[settingNames[i]] = settingValues[i]
    raidWeekendsAdded.append(sheetSettings["raidWeekendsAdded"])

def entire_row(row):
    return f"{row}:{row}"
def entire_column(column):
    return f"{column}:{column}"


def cell_range_row():
    pass


def cell_range_column(column,start,end,offset):
    return f"{column}{start+offset}:{column}{end+offset}"

def column_to_number(columnNum):
    result = []
    while columnNum > 0:
        columnNum, remainder = divmod(columnNum - 1, 26)
        result.append(chr(remainder + ord('A')))
    return ''.join(reversed(result))