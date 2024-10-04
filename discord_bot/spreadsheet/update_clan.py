import sys
import os
from discord_bot.spreadsheet import spreadsheet as sheet


script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
project_dir = os.path.dirname(parent_dir)
# Add the project root directory to sys.path

sys.path.append(project_dir)

from discord_bot.spreadsheet.sheets import members, war, capital, games, cwl

def update_clan_spreadsheet():
    members.update_member_sheet()

    war.update_war_sheet()
    capital.update_raid_sheet()
    cwl.update_cwl_sheet()
    games.update_games_sheet()