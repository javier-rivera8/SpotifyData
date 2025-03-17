import json
import psycopg2

# Database connection parameters
DB_NAME = "spotify_db"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"

# Load JSON data from file
with open("files/Streams2024.json", "r", encoding="utf-8") as file:
    data = json.load(file)  # Only take the first 5 elements

# Connect to PostgreSQL
def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# Create table if not exists
def create_table():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS spotify_tracks (
                    id SERIAL PRIMARY KEY,
                    track_name TEXT,
                    artist_name TEXT,
                    album_name TEXT,
                    ts TIMESTAMP
                )
            """)
            conn.commit()

# Insert data into table
def insert_data():
    with connect_db() as conn:
        with conn.cursor() as cur:
            for entry in data:
                track_name = entry.get("master_metadata_track_name")
                artist_name = entry.get("master_metadata_album_artist_name")
                album_name = entry.get("master_metadata_album_album_name")
                ts = entry.get("ts")
                skipped = entry.get("skipped", False)
                
                if track_name and artist_name and album_name and ts and not skipped:
                    cur.execute(
                        "INSERT INTO spotify_tracks (track_name, artist_name, album_name, ts) VALUES (%s, %s, %s, %s)",
                        (track_name, artist_name, album_name, ts)
                    )
            conn.commit()

if __name__ == "__main__":
    create_table()
    insert_data()
    print("Successfully!")
