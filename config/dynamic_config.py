import argparse
from config.config import config  # Import the shared config
import discord_bot.spreadsheet.spreadsheet as sheet


def update_config_with_args():
    parser = argparse.ArgumentParser(description="A script that accepts a tag and an ID.")
    parser.add_argument('tag', type=str, help='A tag (string input, no #)')
    parser.add_argument('id', type=str, help='Your sheet ID (string input)')
    # Parse the arguments
    args = parser.parse_args()
    # Store the arguments in variables
    tag = args.tag
    sheet_id = args.id

    # Update config based on command-line arguments if provided
    if tag is not None:
        config['clan_tag'] = tag
    if sheet_id is not None:
        config['sheet_id'] = sheet_id


def update_config_with_sheet_settings():
    setting_names, setting_values = sheet.get_sheet_settings()
    for i in range (0, len(setting_names)):
        config[setting_names[i]] = setting_values[i]
