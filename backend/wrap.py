import json
import psycopg2
from collections import defaultdict

DB_NAME = "spotify_db"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"

def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def fetch_songs(table_name):
    song_cnt = defaultdict(int)
    conn = connect_db()
    cursor = conn.cursor()
    
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    
    rows = cursor.fetchall()
    
    for row in rows:
        song_cnt[row[1]] += 1
    
    cursor.close()
    conn.close()
    max_cnt = 0
    max_key = ""
    for key, value in song_cnt.items():
        if value > max_cnt:
            max_cnt = value
            max_key = key
    print(max_key)
    print(max_cnt)

if __name__ == "__main__":
    fetch_songs("spotify_tracks")  
