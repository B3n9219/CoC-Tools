class Player():
    def __init__(self, name, tag, role=None, th_level=None, clan_status=None, raid_attacks = 0, gold_looted = 0):
        self.name = name
        self.tag = tag
        self.role = role
        self.th_level = th_level
        self.clan_status = clan_status
        self.raid_attacks = raid_attacks
        self.gold_looted = gold_looted

    def __str__(self):
        return f"name: {self.name}, tag: {self.tag}"

    def __repr__(self):
        return str(self)

    def is_player_equal_to(self,player):
        if player.tag == self.tag:
            return True
        else:
            return False

    def is_player_in_list(self, player_list):
        for player in player_list:
            if self.is_player_equal_to(player):
                return True
        return False
