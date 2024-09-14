class ClanInfo():
    def __init__(self, tag: object, clan_name: object = None, sheet_id: object = None, server_id: object = None) -> object:
        self.tag = tag
        self.clan_name = clan_name
        self.sheet_id = sheet_id
        self.server_id = server_id
    def to_dict(self):
        dict = {"tag": self.tag,
                "clan_name": self.clan_name,
                "sheet_id": self.sheet_id,
                "server_id": self.server_id
        }
        return dict

#HELLO
