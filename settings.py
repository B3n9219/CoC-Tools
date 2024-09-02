import spreadsheet as sheet
from datetime import *
from dateutil.relativedelta import relativedelta
import argparse

currentDate = datetime.now()

apiKey = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjZhZDAyZTc1LWIzMjctNGM3Yi1iNzljLWJiOTNkMzY4MWYyMyIsImlhdCI6MTcyMzMwMjMzMiwic3ViIjoiZGV2ZWxvcGVyL2E1Yjc0NTA2LWI3ZDQtZmE3OC0yMmU1LTMwYTg3OTM3YzBlYiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE0Ny4xNDcuOTIuNDMiXSwidHlwZSI6ImNsaWVudCJ9XX0.tObIRu64OrHg2tVMB6Ry4SPBGWQIvsRJNto3Z_9IO8V0pUMGgJoXRgLQl6phL_4sGGyVfYVpclo0Dre3e438YA"
baseRequest = "https://api.clashking.xyz"
playerRequestURL = f"{baseRequest}/player/%23"  #followed by player tag (no #)
clanRequestURL = f"{baseRequest}/v1/clans/%23"  #followed by clan tag (no #)

def get_command_line_inputs():
    parser = argparse.ArgumentParser(description="A script that accepts a tag and an ID.")
    parser.add_argument('tag', type=str, help='A tag (string input, no #)')
    parser.add_argument('ID', type=str, help='Your sheet ID (string input)')
    # Parse the arguments
    args = parser.parse_args()
    # Store the arguments in variables
    tag = args.tag
    sheet_ID = args.ID
    # Output the stored variables (optional)
    print(f"Tag: {tag}")
    print(f"ID: {sheet_ID}")
    return tag, sheet_ID


clanTag, SPREADSHEET_ID = get_command_line_inputs()


#The Fireflies:
#clanTag = "2R989CY89"
#SPREADSHEET_ID = "1reUNArwTCosIrk67yqSHPu5P5F06LWDdAXb14rf0AEw"

#The Fireflies 2:
#clanTag = "2RLQPCVO8"
#SPREADSHEET_ID = "1i4axEHp1-1PTHNJ_NKNb5ZMH58_ljz08feGyKRZofro"

#The Bureau
#clanTag = "2G0RLQ9J0"
#SPREADSHEET_ID = "1ATDoewJG9UXnwtKvp8yrrGLgeSdps9dHlTsXZiIOh70"

#The Real
#clanTag = "822VUL29"
#SPREADSHEET_ID = "13dUQ7paaWoYbe9oEdWy9tkp5PVsQDizD8J6L5XX2BWk"

#SKILL MAN
#clanTag = "VVQ8VLPC"
#SPREADSHEET_ID = "1oxlTAXwYyd6fJdAIfAAnqc7aaKZlWuct8RIZ2KpzMsg"

#Dark Alliance
#clanTag = "Q8CY8LYV"
#SPREADSHEET_ID = "1tlkV018ijrKsJVNUOyz-cusBYRY2-shVNECC8g9Tu1Y"

#The Shamrocks
#clanTag = "8R9VQQ8Q"
#SPREADSHEET_ID = "170i6nXjqdALylhcu_ufGZCKylefI3eidQcbqoFOOEZM"


columns_per_CWL = 5
CWL_info_columns = 7
war_info_columns = 6

title_row_offset = 2

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
clanStatusColumn = "C"
roleColumn = "D"
THLevelColumn = "E"

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


def entire_column(column):
    return f"{column}:{column}"

def column_to_number(columnNum):
    result = []
    while columnNum > 0:
        columnNum, remainder = divmod(columnNum - 1, 26)
        result.append(chr(remainder + ord('A')))
    return ''.join(reversed(result))