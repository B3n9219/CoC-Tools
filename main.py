import sys
import os

import config.dynamic_config as dynamic_config  # Import function for updating config
from config.config import config  # Import the shared config
from discord_bot.spreadsheet.update_clan import update_clan_spreadsheet

if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.abspath(__file__))
    print(project_dir)
    sys.path.append(project_dir)
    # Update config with command-line arguments (if provided)
    dynamic_config.update_config_with_args()
    dynamic_config.update_config_with_sheet_settings()
    # Use the updated config
    #print(f"Config: {config}")
    print(f"Starting application with tag: {config['clan_tag']}")
    print(f"Starting application with spreadsheet: {config['sheet_id']}")
    update_clan_spreadsheet()



