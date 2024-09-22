import json
import os


def load_static_config(config_file='config.json'):
    # Get the directory of the current file (config.py)
    base_dir = os.path.dirname(__file__)

    # Construct the full path to the config.json file
    full_path = os.path.join(base_dir, config_file)

    with open(full_path, 'r') as file:
        return json.load(file)


# Initialize the config
config = load_static_config()
print(config)


