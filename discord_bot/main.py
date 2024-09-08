from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands


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


@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}",
                                            ephemeral=True)


@bot.tree.command(name="add_clan")
@app_commands.describe(tag="clan tag")
async def display_clan(interaction: discord.Interaction, tag: str):
    await interaction.response.send_message(f"{interaction.user.mention}'s clan is {tag}")


# MAIN CODE
def main() -> None:
    bot.run(token=TOKEN)


if __name__ == "__main__":
    main()
