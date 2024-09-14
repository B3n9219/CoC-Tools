from google.cloud import storage
import json
from discord_bot.spreadsheet import spreadsheet as sheet
from discord_bot.server.service_key import *

#serviceKey_folder = r"G:\.shortcut-targets-by-id\0BxLsm2sliUVxS3JlODdPbFFwOEU\Ben\Clan Management Sheet\SSH Keys"
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(serviceKey_folder, 'ServiceKey_GoogleCloud.json')

storage_client = storage.Client()
coc_tools_bucket_name = 'coc-tools-files'
clan_file = 'clans.json'

current_dir = os.path.dirname(os.path.abspath(__file__))

coc_tools_bucket = storage_client.bucket(coc_tools_bucket_name)
clan_json_blob = coc_tools_bucket.blob('clans.json')


def convert_file_to_dict():
    #clan_info_json = clan_json_blob.download_as_text()
    #clan_info_dict = json.loads(clan_info_json)
    clan_info_json = open(os.path.join(current_dir, 'temp', 'clans.json'))
    clan_info_dict = json.load(clan_info_json)
    return clan_info_dict


def create_clan_spreadsheet(clan_info, clans_on_server):
    if clan_info.tag in clans_on_server:
        if clans_on_server[clan_info.tag]["sheet_id"] == None:
            print("clan has been added but no spreadsheet")
            print("Creating spreadsheet...")
            sheet_id = sheet.make_spreadsheet(clan_info.clan_name)
            clan_info.sheet_id = sheet_id
        else:
            clan_info.sheet_id = clans_on_server[clan_info.tag]["sheet_id"]
    else:
        print("Creating spreadsheet...")
        sheet_id = sheet.make_spreadsheet(clan_info.clan_name)
        clan_info.sheet_id = sheet_id
    print(clan_info.sheet_id)
    return clan_info


def add_clan_to_server(clan_info):
    # Initialize the client
    client = storage.Client()
    bucket = client.bucket(coc_tools_bucket_name)
    blob = bucket.blob(clan_file)




    # Step 1: Download the existing blob content
    local_file_path = os.path.join(current_dir, 'temp', 'clans.json')

    blob.download_to_filename(local_file_path)  #downloads the server clans.json to the local clans.json
    with open(local_file_path, 'r') as file:
        json_text = file.read()
    clans_on_server = json.loads(json_text)

    clan_info = create_clan_spreadsheet(clan_info, clans_on_server)
    clan_info_dict = clan_info.to_dict()
    #clan_dict = {clan_info.tag: clan_info_dict}

    clans_on_server[clan_info.tag] = clan_info_dict   #adding the new clan to the dictionary of clans on the server
    json_to_add = json.dumps(clans_on_server, indent=4)
    # Step 2: Append the new data locally
    with open(local_file_path, 'w') as file:
        file.write(json_to_add)

    # Step 3: Upload the updated file back to the bucket
    blob.upload_from_filename(local_file_path)

    print("Data appended and uploaded successfully.")
    return clan_info

#clan = ClanInfo(tag="#2R989CY89", clan_name="The fireflies", sheet_id=None)
#add_clan_to_server(clan)
