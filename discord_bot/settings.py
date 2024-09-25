from datetime import *
from dateutil.relativedelta import relativedelta


#currentDate = datetime.now()


def update_settings(sheet_settings):
    global raidWeekendsAdded
    settingNames = sheet_settings[0]
    settingValues = sheet_settings[1]
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


#The Fireflies:
#config["clan_tag"] = "2R989CY89"
#SPREADSHEET_ID = "1reUNArwTCosIrk67yqSHPu5P5F06LWDdAXb14rf0AEw"

#The Fireflies 2:
#config["clan_tag"] = "2RLQPCVO8"

#The Bureau
#config["clan_tag"] = "2G0RLQ9J0"
#SPREADSHEET_ID = "1ATDoewJG9UXnwtKvp8yrrGLgeSdps9dHlTsXZiIOh70"

#The Real
#config["clan_tag"] = "822VUL29"
#SPREADSHEET_ID = "13dUQ7paaWoYbe9oEdWy9tkp5PVsQDizD8J6L5XX2BWk"

#SKILL MAN
#config["clan_tag"] = "VVQ8VLPC"
#SPREADSHEET_ID = "1oxlTAXwYyd6fJdAIfAAnqc7aaKZlWuct8RIZ2KpzMsg"

#Dark Alliance
#config["clan_tag"] = "Q8CY8LYV"
#SPREADSHEET_ID = "1tlkV018ijrKsJVNUOyz-cusBYRY2-shVNECC8g9Tu1Y"

#The Shamrocks
#config["clan_tag"] = "8R9VQQ8Q"
#SPREADSHEET_ID = "170i6nXjqdALylhcu_ufGZCKylefI3eidQcbqoFOOEZM"