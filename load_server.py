import os
from google.cloud import storage

serviceKey_folder = r"G:\.shortcut-targets-by-id\0BxLsm2sliUVxS3JlODdPbFFwOEU\Ben\Clan Management Sheet\SSH Keys"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(serviceKey_folder, 'ServiceKey_GoogleCloud.json')

storage_client = storage.Client()

bucket_name = 'coc-tools-files'
bucket = storage_client.bucket(bucket_name)

CLAN_LIST = bucket.blob('clans.txt').download_as_text()
print(CLAN_LIST)
