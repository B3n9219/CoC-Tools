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


async def clan_autocomplete(interaction: discord.Interaction, current: str):
    clans = server.retrieve_clans_from_server()
    # Suggest clans that match the user's input
    suggestions = []
    # Loop through each clan in the list
    for clan in clans:
        # Check if the user's input (current) matches part of the clan name (case-insensitive)
        if current.lower() in clan.lower():
            # Add a matching clan as an app_commands.Choice to the suggestions list
            suggestions.append(app_commands.Choice(name=f"{clans[clan]['clan_name']} | {clan}", value=clan))
        # Limit the number of suggestions to 25
        if len(suggestions) >= 10:
            break

    # Return the suggestions list
    return suggestions




def setup_commands(bot: commands.Bot) -> None:
    @bot.tree.command(name="add_clan")
    @app_commands.describe(tag="clan tag")
    async def add_clan(interaction: discord.Interaction, tag: str):
        await interaction.response.defer(ephemeral=True)
        if check_if_clan_exists(tag[1:]) == True:
            clan_name = get_clan_name(tag[1:])
            clan = ClanInfo(tag=tag, clan_name=clan_name, sheet_id=None, server_id=interaction.guild_id)
            server.add_clan_to_server(clan)
            await interaction.followup.send(f"{interaction.user.mention} your clan {clan.clan_name}({clan.tag}) has been added to the server. \n"
                                            f"use /make_spreadsheet to create yourself a clan management spreadsheet.", ephemeral=True)
        else:
            await interaction.followup.send(
                f"{interaction.user.mention} the clan {tag} does not exist")


    @bot.tree.command(name="make_spreadsheet")
    @app_commands.describe(tag="clan tag")
    @app_commands.autocomplete(tag=clan_autocomplete)
    async def make_spreadsheet(interaction: discord.Interaction, tag: str):
        await interaction.response.defer(ephemeral=True)
        if check_if_clan_exists(tag[1:]) == True:
            clan_name = get_clan_name(tag[1:])
            clan = ClanInfo(tag=tag, clan_name=clan_name, sheet_id=None, server_id=interaction.guild_id)
            server_clan_info = server.get_clan_info_from_server(tag)
            if server.get_clan_info_from_server(tag) is not None:
                if server_clan_info["sheet_id"] is None:
                    clan.sheet_id = server.create_clan_spreadsheet(clan)
                    server.add_clan_to_server(clan)
                    await interaction.followup.send(
                        f"{interaction.user.mention} your clan {clan.clan_name}({clan.tag}) has been added. \n"
                        f"This is your clan spreadsheet link : https://docs.google.com/spreadsheets/d/{clan.sheet_id}/edit  \n"
                        f"The sheet will be updating with your clan's data now", ephemeral=True)
                    dynamic_config.update_config_with_clan_settings(clan.tag[1:], clan.sheet_id)
                    dynamic_config.update_config_with_sheet_settings()
                    await asyncio.to_thread(update_clan_spreadsheet)
                else:
                    clan.sheet_id = server_clan_info["sheet_id"]
                    await interaction.followup.send(
                        f"{interaction.user.mention} your clan {clan.clan_name}({clan.tag}) has already been added. \n"
                        f"This is your clan spreadsheet link : https://docs.google.com/spreadsheets/d/{clan.sheet_id}/edit", ephemeral=True)
            else:
                await interaction.followup.send(f"Clan {tag} is not linked yet.  Use /add_clan to link your clan first", ephemeral=True)
        else:
            await interaction.followup.send(f"Clan {tag} does not exist", ephemeral=True)

    @bot.tree.command(name="display_spreadsheet")
    @app_commands.describe(tag="clan tag")
    @app_commands.autocomplete(tag=clan_autocomplete)
    async def display_spreadsheet(interaction: discord.Interaction, tag: str):
        await interaction.response.defer(ephemeral=True)
        clan_info = server.get_clan_info_from_server(tag)
        if clan_info is not None:
            if clan_info["sheet_id"] is not None:
                await interaction.followup.send(f"{interaction.user.mention} This is the spreadsheet for your clan {clan_info['clan_name']}({clan_info['tag']}) \n"
                                                f"https://docs.google.com/spreadsheets/d/{clan_info['sheet_id']}/edit")
            else:
                await interaction.followup.send(
                    f"{interaction.user.mention} Your clan {clan_info['clan_name']}({clan_info['tag']}) has no spreadsheet made for it.\n"
                    f"use /make_spreadsheet to make one")

        else:
            if check_if_clan_exists(tag[1:]):
                await interaction.followup.send(
                    f"{interaction.user.mention} the clan {tag} is not on the server, use /add_clan first")
            else:
                await interaction.followup.send(
                    f"{interaction.user.mention} the clan {tag} does not exist")



    @bot.tree.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(interaction: discord.Interaction):
        await interaction.response.send_message("Shutting down the bot...", ephemeral=True)
        await bot.close()
