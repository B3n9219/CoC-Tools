import os
import subprocess
import json
import datetime

os.chdir("/home/benkirk1441/cloud_storage/CoC-Tools/discord_bot/spreadsheet/dist")

cloud_folder = "/home/benkirk1441/cloud_storage"

clan_list = os.path.join(cloud_folder, "clans.json")
run_log = os.path.join(cloud_folder, "logs", "run_log.txt")
output_log = os.path.join(cloud_folder, "logs", "output_log.txt")

#clan_list = "discord_bot/server/temp/clans.json"

with open(clan_list, 'rb') as file:
    blob_data = file.read()
    json_string = blob_data.decode('utf-8')
    clan_info = json.loads(json_string)
    for clan in clan_info:
        with open(run_log, 'a') as log_file:
            log_file.write(f"{datetime.now()} - Updating clan: {clan.name}({clan.tag})\n")

            # Run the ELF binary and capture output
        try:
            with open(output_log, 'w') as output_file:
                result = subprocess.run(
                    ['./main', clan.tag, clan.sheet_id],
                    stdout=output_file,
                    stderr=subprocess.STDOUT,
                    text=True
                )

            # Check if the process was successful
            if result.returncode != 0:
                with open(run_log, 'a') as log_file:
                    log_file.write(f"{datetime.now()} - Error occurred with tag: {clan.tag} and ID: {clan.name}\n")
            else:
                with open(run_log, 'a') as log_file:
                    log_file.write(f"{datetime.now()} - Successfully updated clan with tag: {clan.tag} and ID: {clan.name}\n")

        except Exception as e:
            with open(run_log, 'a') as log_file:
                log_file.write(f"{datetime.now()} - Exception occurred: {str(e)}\n")