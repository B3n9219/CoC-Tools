class Player():
    def __init__(self, name, tag, clan_status=None, role=None, th_level=None, war_attacks = 0, raid_attacks = 0,
                 gold_looted = 0, games_score = 0, cwl_stars = 0, cwl_attacks_used = 0, cwl_attacks_available = 0):
        self.name = name
        self.tag = tag
        self.clan_status = clan_status
        self.role = role
        self.th_level = th_level
        self.war_attacks = war_attacks
        self.raid_attacks = raid_attacks
        self.gold_looted = gold_looted
        self.games_score = games_score
        self.cwl_stars = cwl_stars
        self.cwl_attacks_used = cwl_attacks_used
        self.cwl_attacks_available = cwl_attacks_available

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

    def get_attacks(self, attackType):
        if attackType == "War":
            return self.war_attacks
        if attackType == "Raid":
            return self.raid_attacks
        if attackType == "Games":
            return self.games_score
        if attackType == "Stars":
            return self.cwl_stars
        if attackType == "AttacksUsed":
            return self.cwl_attacks_used
        if attackType == "AttacksAvailable":
            return self.cwl_attacks_available

