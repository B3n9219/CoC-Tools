import os

serviceKey_folder = r"G:\.shortcut-targets-by-id\0BxLsm2sliUVxS3JlODdPbFFwOEU\Ben\Clan Management Sheet\SSH Keys"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(serviceKey_folder, 'ServiceKey_GoogleCloud.json')