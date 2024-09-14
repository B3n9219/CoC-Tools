from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

#script_dir = os.path.dirname(os.path.abspath(__file__))
#parent_dir = os.path.dirname(script_dir)
serviceKey_folder = r"\creds"
#print(os.path.join(parent_dir, r'creds\ServiceKey_GoogleCloud.json'))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(serviceKey_folder, 'ServiceKey_GoogleCloud.json')

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
