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


def read_and_add_clans(json_file, conn):
    with open(json_file, 'r') as file:
        clans_data = json.load(file)
    
    # Iterate over all clans in the JSON
    for clan in clans_data.values():
        tag = clan['tag']
        name = clan['clan_name']
        sheet_id = clan['sheet_id']
        server_id = clan['server_id']
        
        # Add the clan to the database using the provided function
        add_clan_to_db(conn, tag, name, sheet_id, server_id)


# Example usage:
if __name__ == "__main__":
    conn = open_db_connection()
    #player_id = add_player_to_db(conn, 'example_tag', 'John Doe', 'example_clan')
    #if player_id:
    #    print(f"Player added with ID: {player_id}")
    file_path = 'database/temp.json'
    read_and_add_clans(file_path, conn)
    
    close_db_connection(conn)
