from discord import app_commands
from discord.ext import commands
import server.load_server as server
from server.ClanInfo import *
import discord
#import server.test as test
import os
from bot_util import *


def is_tag_in_clan_list(entered_tag: str) -> bool:
    clan_info_dict = server.convert_file_to_dict()
    entered_tag = entered_tag[1:]
    if entered_tag in clan_info_dict:
        print(clan_info_dict[entered_tag])
        return True
    return False


def setup_commands(bot: commands.Bot) -> None:
    @bot.tree.command(name="add_clan")
    @app_commands.describe(tag="clan tag")
    async def display_clan(interaction: discord.Interaction, tag: str):
        #print("CLAN EXISTS:", check_if_clan_exists(tag[1:]))
        if check_if_clan_exists(tag[1:]) == True:
            clan_name = get_clan_name(tag[1:])
            clan = ClanInfo(tag=tag, clan_name=clan_name, sheet_id=None, server_id=interaction.guild_id)
            #await interaction.response.send_message(message, ephemeral=True)
            await interaction.response.defer()
            new_clan_info = server.add_clan_to_server(clan)
            await interaction.followup.send(f"{interaction.user.mention} your clan {new_clan_info.clan_name}({new_clan_info.tag}) has been added. \n"
                                            f"This is your clan spreadsheet link : https://docs.google.com/spreadsheets/d/{new_clan_info.sheet_id}/edit", ephemeral=True)
        else:
            await interaction.followup.send(f"Clan {tag} does not exist", ephemeral=True)