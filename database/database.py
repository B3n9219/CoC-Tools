import psycopg2
from psycopg2 import sql
import json

def open_db_connection():
    """Create and return a database connection."""
    return psycopg2.connect(
        host="localhost", 
        dbname="CoC-Tools", 
        user="postgres",
        password="Oreo9898", 
        port=5432
    )
    
def get_db_players_in_clan(conn, clan):
    with conn.cursor() as cur:
        try:
            print('looking for:', clan)
            cur.execute(
                """SELECT * FROM players WHERE clan_tag = %s;""",
                (clan,)
            )
            conn.commit()  # Commit the transaction
            for row in cur.fetchall():
                print(row)
        except Exception as e:
            conn.rollback()  # Roll back the transaction in case of error
            print(f"Error selecting all players from clan {clan}: {e}") 

def add_player_to_db(conn, tag, name, clan_tag):
    """Adds a player to the database."""    
    with conn.cursor() as cur:
        try:
            cur.execute(
                """INSERT INTO players (tag, name, clan_tag) 
                VALUES (%s, %s, %s);""", 
                (tag, name, clan_tag)
            )
            conn.commit()  # Commit the transaction
        except Exception as e:
            conn.rollback()  # Roll back the transaction in case of error
            print(f"Error adding player: {e}")
        
        
def add_clan_to_db(conn, tag, name, sheet_id, server_id):
    """Adds a clan to the database."""    
    with conn.cursor() as cur:
        try:
            print(tag,name,sheet_id,server_id)
            cur.execute(
                """INSERT INTO clans (tag, name, sheet_id, server_id) 
                VALUES (%s, %s, %s, %s);""", 
                (tag, name, sheet_id, str(server_id))
            )
            conn.commit()  # Commit the transaction
        except Exception as e:
            conn.rollback()  # Roll back the transaction in case of error
            print(f"Error adding clan: {e}")


def close_db_connection(conn):
    """Close the database connection."""
    if conn:
        conn.close()
