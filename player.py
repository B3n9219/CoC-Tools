class Player():
    def __init__(self, name, tag, role=None, th_level=None, clan_status=None):
        self.name = name
        self.tag = tag
        self.role = role
        self.th_level = th_level
        self.clan_status = clan_status

    def __str__(self):
        return f"name: {self.name}, tag: {self.tag}"

    def __repr__(self):
        return str(self)

    def is_player_in_list(self, player_list):
        for player in player_list:
            if player.tag == self.tag:
                return True
        return False