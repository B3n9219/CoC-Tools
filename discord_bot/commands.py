from discord import app_commands
from discord.ext import commands
import server.load_server as server
from server.ClanInfo import *
import discord
#import server.test as test
import os
from main import *


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
            if is_tag_in_clan_list(tag):
                message = f"{interaction.user.mention} your clan ({tag}) has already been added in {interaction.guild}"
                clan = ClanInfo(tag=tag, clan_name=clan_name, sheet_id=None, server_id=interaction.guild_id)
            else:
                message = f"{interaction.user.mention} your clan ({tag}) has been added in {interaction.guild}"
                clan = ClanInfo(tag=tag, clan_name=clan_name, sheet_id=None, server_id=interaction.guild_id)
            await interaction.response.send_message(message, ephemeral=True)
            server.add_clan_to_server(clan)
        else:
            await interaction.response.send_message(f"Clan {tag} does not exist", ephemeral=True)