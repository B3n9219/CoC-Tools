import members
from settings import *
import capital
import war
import games
import cwl
import spreadsheet as sheet


sheet_settings = sheet.get_sheet_settings()
update_settings(sheet_settings)
members.update_member_sheet()

war.update_war_sheet()
capital.update_raid_sheet()

cwl.update_cwl_sheet()
games.update_games_sheet()