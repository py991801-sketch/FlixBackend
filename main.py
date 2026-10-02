from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import urllib.parse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "online", "message": "FlixTime Clean Torrent API is Running!"}

@app.get("/find_hindi_movie")
def find_hindi_movie(title: str):
    try:
        query = title.strip()
        
        # 1. APIBay (Official Pirate Bay API) ka use karna (No Ads, No Fake Links)
        # Hindi movies dhoondhne ke liye query me 'hindi' jod diya
        api_url = f"https://apibay.org/q.php?q={urllib.parse.quote(query + ' hindi')}"
        response = requests.get(api_url, timeout=10)
        
        magnet_link = None
        if response.status_code == 200:
            data = response.json()
            # Agar koi result mila aur wo fake result nahi hai (00000 hash wala)
            if len(data) > 0 and data[0].get("info_hash") != "0000000000000000000000000000000000000000":
                info_hash = data[0]["info_hash"]
                movie_name = data[0]["name"]
                
                # Asli Magnet link khud banayenge API data se
                magnet_link = f"magnet:?xt=urn:btih:{info_hash}&dn={urllib.parse.quote(movie_name)}"

        # 2. Magnet ko Webtor player me dalna
        if magnet_link:
            stream_url = f"https://webtor.io/show?magnet={urllib.parse.quote(magnet_link)}"
            return {
                "status": "success",
                "title": query,
                "type": "embed",
                "server1": stream_url,
                "server2": f"https://vidsrc.to/embed/movie/{urllib.parse.quote(query)}",
                "server3": f"https://autoembed.co/movie/tmdb/0?q={urllib.parse.quote(query)}"
            }

        # Fallback agar API par Hindi Torrent na mile
        return {
            "status": "success",
            "title": query,
            "type": "embed",
            "server1": f"https://vidsrc.to/embed/movie/{urllib.parse.quote(query)}",
            "server2": f"https://autoembed.co/movie/tmdb/0?q={urllib.parse.quote(query)}",
            "server3": f"https://vidsrc.me/embed/movie/{urllib.parse.quote(query)}"
        }

    except Exception as e:
        return {
            "status": "success",
            "title": title,
            "type": "embed",
            "server1": f"https://vidsrc.to/embed/movie/0",
            "server2": f"https://autoembed.co/movie/tmdb/0",
            "server3": f"https://vidsrc.me/embed/movie/0"
        }
        
