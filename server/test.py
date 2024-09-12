import server.load_server as server
from server.ClanInfo import *

clan1 = ClanInfo("#001", "The Fireflies")
clan2 = ClanInfo("#002", "The Fireflies")

server.add_clan_to_server(clan1)
server.add_clan_to_server(clan2)

def add_clan(clan):
    try:
        server.add_clan_to_server(clan)
    except Exception as e:
        print("AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        print(e)