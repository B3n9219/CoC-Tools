from discord import app_commands
from discord.ext import commands
import discord_bot.server.load_server as server
from discord_bot.server.ClanInfo import *
import discord
import config.dynamic_config as dynamic_config  # Import function for updating config
from config.config import config  # Import the shared config
from utilities.bot_util import *
from discord_bot.spreadsheet.update_clan import update_clan_spreadsheet
import asyncio


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
        await interaction.response.defer(ephemeral=True)
        if check_if_clan_exists(tag[1:]) == True:
            clan_name = get_clan_name(tag[1:])
            clan = ClanInfo(tag=tag, clan_name=clan_name, sheet_id=None, server_id=interaction.guild_id)
            #await interaction.response.send_message(message, ephemeral=True)
            new_clan_info = server.add_clan_to_server(clan)
            await interaction.followup.send(f"{interaction.user.mention} your clan {new_clan_info.clan_name}({new_clan_info.tag}) has been added. \n"
                                            f"This is your clan spreadsheet link : https://docs.google.com/spreadsheets/d/{new_clan_info.sheet_id}/edit  \n"
                                            f"The sheet will be updating with your clan's data now", ephemeral=True)
            dynamic_config.update_config_with_clan_settings(new_clan_info.tag[1:], new_clan_info.sheet_id)
            dynamic_config.update_config_with_sheet_settings()
            await asyncio.to_thread(update_clan_spreadsheet)
            #interaction.followup.send(f"{interaction.user.mention} your clan spreadsheet has been updated with your clan's data", ephemeral=True)
        else:
            await interaction.followup.send(f"Clan {tag} does not exist", ephemeral=True)