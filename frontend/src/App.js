import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const CLIENT_ID = "192ead2715344c5dad29c0d2f13143af";
const REDIRECT_URI = "http://localhost:3000";
const AUTH_ENDPOINT = "https://accounts.spotify.com/authorize";
const RESPONSE_TYPE = "token";
const SCOPE = "user-read-recently-played";
const BACKEND_URL = "http://localhost:8000/tracks/"; // FastAPI Backend URL

function App() {
  const [token, setToken] = useState("");
  const [tracks, setTracks] = useState([]);

  useEffect(() => {
    const hash = window.location.hash;
    if (hash) {
      const tokenFromUrl = new URLSearchParams(hash.substring(1)).get(
        "access_token"
      );
      if (tokenFromUrl) {
        setToken(tokenFromUrl);
        localStorage.setItem("spotify_token", tokenFromUrl);
        window.location.hash = "";
      }
    }

    const storedToken = localStorage.getItem("spotify_token");
    if (storedToken) {
      setToken(storedToken);
    }
  }, []);

  const getRecentlyPlayedTracks = async () => {
    if (!token) return;
    try {
      const response = await axios.get(
        "https://api.spotify.com/v1/me/player/recently-played?limit=50",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setTracks(response.data.items);

      // Send tracks to FastAPI backend
      for (const item of response.data.items) {
        const trackData = {
          name: item.track.name,
          artist: item.track.artists.map((artist) => artist.name).join(", "),
          album: item.track.album.name,
          image_url: item.track.album.images[0]?.url || "",
        };

        await axios.post(BACKEND_URL, trackData)
          .then(() => console.log("Track saved:", trackData))
          .catch((error) => console.error("Error saving track:", error));
      }
    } catch (error) {
      console.error("Error fetching recently played tracks:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h2>Spotify Recent Tracks</h2>

        {!token ? (
          <a
            className="login-button"
            href={`${AUTH_ENDPOINT}?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=${RESPONSE_TYPE}&scope=${SCOPE}`}
          >
            Login to Spotify
          </a>
        ) : (
          <>
            <button onClick={getRecentlyPlayedTracks}>Show Recently Played</button>
            <button
              onClick={() => {
                setToken("");
                localStorage.removeItem("spotify_token");
              }}
            >
              Logout
            </button>

            <ul>
              {tracks.map((track, index) => (
                <li key={index}>
                  <img
                    src={track.track.album.images[0]?.url}
                    alt="Album Cover"
                    width="50"
                  />
                  <p>
                    {track.track.name} - {track.track.artists.map((artist) => artist.name).join(", ")}
                  </p>
                </li>
              ))}
            </ul>
          </>
        )}
      </header>
    </div>
  );
}

export default App;
