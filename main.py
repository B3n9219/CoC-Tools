import requests
import spreadsheet as sheet
import members
from settings import *
import capital
import war
import games
import cwl


#updates the member sheet's member list
update_settings()
members.update_member_sheet()

war.update_war_sheet()
capital.update_raid_sheet()

cwl.update_cwl_sheet()
games.update_games_sheet()