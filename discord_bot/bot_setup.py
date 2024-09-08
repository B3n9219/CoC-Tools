from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Load environment variables
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot setup
intents: discord.Intents = discord.Intents.default()
intents.message_content = True   # NOQA
bot = commands.Bot(command_prefix="!", intents=intents)

# Import commands after bot setup to avoid circular imports
from commands import setup_commands

# Setup commands
setup_commands(bot)

# Event handling
@bot.event
async def on_ready() -> None:
    print(f"{bot.user} is now running!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


def main() -> None:
    bot.run(token=TOKEN)


if __name__ == "__main__":
    main()
