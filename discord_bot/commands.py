from discord import app_commands
from discord.ext import commands
from load_server import CLAN_LIST
import discord

def is_tag_in_clan_list(entered_tag: str) -> bool:
    entered_tag = entered_tag[1:]
    for clan in CLAN_LIST.splitlines():
        clan_tag = clan.split('\t')[0]
        if clan_tag == entered_tag:
            return True
    return False

def setup_commands(bot: commands.Bot) -> None:
    @bot.tree.command(name="add_clan")
    @app_commands.describe(tag="clan tag")
    async def display_clan(interaction: discord.Interaction, tag: str):
        if is_tag_in_clan_list(tag):
            message = f"{interaction.user.mention} your clan ({tag}) has already been added"
        else:
            message = f"{interaction.user.mention} your clan ({tag}) has been added"
        await interaction.response.send_message(message, ephemeral=True)
