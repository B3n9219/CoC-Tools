import os
import subprocess
import json
from datetime import datetime

creds_path = "/home/benkirk1441/cloud_storage/creds/credentials.json"
cloud_folder = "/home/benkirk1441/cloud_storage"
update_clan_elf = "/home/benkirk1441/elf/update_clan"
update_clan_python = "/home/benkirk1441/cloud_storage/CoC-Tools/main.py"
clan_list = os.path.join(cloud_folder, "clans.json")
run_log = os.path.join(cloud_folder, "logs", "run_log.txt")
output_log = os.path.join(cloud_folder, "logs", "output_log.txt")

#clan_list = "discord_bot/server/temp/clans.json"

with open(clan_list, 'rb') as file:
    blob_data = file.read()
    json_string = blob_data.decode('utf-8')
    clan_info = json.loads(json_string)
    for clan in clan_info.values():
        clan_tag = clan.get("tag")[1:]
        clan_name = clan.get("clan_name")
        sheet_id = clan.get("sheet_id")
        with open(run_log, 'a') as log_file:
            log_file.write(f"{datetime.now()} - Updating clan: {clan_name}({clan_tag})\n")

            # Run the ELF binary and capture output
        try:
            with open(output_log, 'w') as output_file:
                result = subprocess.run(
                    ["python3", update_clan_python, clan_tag, sheet_id],
                    stdout=output_file,
                    stderr=subprocess.STDOUT,
                    text=True
                )

            # Check if the process was successful
            if result.returncode != 0:
                error_log = os.path.join(os.path.join(cloud_folder,"logs","error_logs"), f"error_log_{clan_tag}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
                with open(error_log, 'w') as error_file:
                    error_file.write(f"Error occurred with tag: {clan_tag} and ID: {sheet_id}\n")
                    error_file.write(f"Timestamp: {datetime.now()}\n\n")
                    # Append the contents of the output log to the error log
                    with open(output_log, 'r') as output_file:
                        error_file.write(output_file.read())
                with open(run_log, 'a') as log_file:
                    log_file.write(f"{datetime.now()} - Error occurred with tag: {clan_tag} and ID: {sheet_id}\n")
            else:
                test_output_log = os.path.join(os.path.join(cloud_folder, "logs", "output_logs"),
                                         f"output_log_{clan_tag}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
                with open(test_output_log, 'w') as test_output_file:
                    with open(output_log, 'r') as output_file:
                        test_output_file.write(output_file.read())
                with open(run_log, 'a') as log_file:
                    log_file.write(f"{datetime.now()} - Successfully updated clan with tag: {clan_tag} and ID: {sheet_id}\n")

        except Exception as e:
            with open(run_log, 'a') as log_file:
                log_file.write(f"{datetime.now()} - Exception occurred: {str(e)}\n")