from discord_bot.spreadsheet.sheets import members, war, capital, games, cwl
from discord_bot.spreadsheet import spreadsheet as sheet
from discord_bot.settings import *

sheet_settings = sheet.get_sheet_settings()
update_settings(sheet_settings)
members.update_member_sheet()

war.update_war_sheet()
capital.update_raid_sheet()

cwl.update_cwl_sheet()
games.update_games_sheet()