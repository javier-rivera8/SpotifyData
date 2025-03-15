from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware

# Database connection
DATABASE_URL = "postgresql://postgres:1234@localhost/spotify_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Track model
class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    album = Column(String, nullable=False)
    image_url = Column(String)

# Function to create the table if it doesn't exist
def create_tables():
    inspector = inspect(engine)
    if "tracks" not in inspector.get_table_names():
        Base.metadata.create_all(bind=engine)

# Ensure tables exist
create_tables()

# FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class TrackCreate(BaseModel):
    name: str
    artist: str
    album: str
    image_url: str

@app.post("/tracks/")
def save_track(track: TrackCreate):
    create_tables()  # Ensure table exists before inserting
    db = SessionLocal()
    db_track = Track(
        name=track.name,
        artist=track.artist,
        album=track.album,
        image_url=track.image_url
    )
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    db.close()
    return {"message": "Track saved successfully"}
