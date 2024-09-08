from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
from load_server import CLAN_LIST

# STEP 0: LOAD TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# STEP 1: BOT SETUP
intents: discord.Intents = discord.Intents.default()
intents.message_content = True   # NOQA
bot = commands.Bot(command_prefix="!", intents=intents)


# STEP 2: HANDLING THE STARTUP FOR THE BOT:
@bot.event
async def on_ready() -> None:
    print(f"{bot.user} is now running!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.tree.command(name="add_clan")
@app_commands.describe(tag="clan tag")
async def display_clan(interaction: discord.Interaction, tag: str):
    if is_tag_in_clan_list(tag):
        message = f"{interaction.user.mention} your clan ({tag}) has already been added"
    else:
        message = f"{interaction.user.mention} your clan ({tag}) has been added"
    await interaction.response.send_message(message, ephemeral=True)


# MAIN CODE
def is_tag_in_clan_list(entered_tag):
    entered_tag = entered_tag[1:]
    for clan in CLAN_LIST.splitlines():
        clan_tag = clan.split('\t')[0]
        if clan_tag == entered_tag:
            return True
    return False

def main() -> None:
    bot.run(token=TOKEN)


if __name__ == "__main__":
    main()
