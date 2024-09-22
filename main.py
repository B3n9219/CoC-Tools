from config.dynamic_config import update_config_with_args  # Import function for updating config
from config.config import config  # Import the shared config

if __name__ == "__main__":
    # Update config with command-line arguments (if provided)
    update_config_with_args()
    # Use the updated config
    print(f"Starting application with tag: {config["clan_tag"]}")
    print(f"Starting application with spreadsheet: {config["sheet_id"]}")


