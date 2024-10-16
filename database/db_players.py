import database as db
import player

def get_players_in_db(conn, clan):
    """gets the players in the spreadsheet who are in a given clan"""
    
    
conn = db.open_db_connection()
db.get_db_players_in_clan(conn, '#2R989CY89')
db.close_db_connection(conn)