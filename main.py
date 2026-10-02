from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
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
    return {"status": "online", "message": "FlixTime PirateBay Streaming Engine is Running!"}

@app.get("/find_hindi_movie")
def find_hindi_movie(title: str):
    try:
        query = title.strip()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        # 1. The Pirate Bay se search karna (Hindi keyword ke sath)
        search_query = urllib.parse.quote(f"{query} hindi")
        tpb_url = f"https://www.thepiratebay3.site/search.php?q={search_query}"
        
        response = requests.get(tpb_url, headers=headers, timeout=15)
        
        magnet_link = None
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Pehla magnet link dhoondhna
            for a in soup.find_all('a', href=True):
                if a['href'].startswith('magnet:?'):
                    magnet_link = a['href']
                    break

        # 2. Agar Magnet Link mil gaya toh use direct Webtor Streaming Player me convert kar do
        if magnet_link:
            stream_url = f"https://webtor.io/show?magnet={urllib.parse.quote(magnet_link)}"
            return {
                "status": "success",
                "title": query,
                "type": "embed",
                "server1": stream_url, # Server 1 ab seedha Pirate Bay ka magnet stream karega
                "server2": f"https://vidsrc.to/embed/movie/{urllib.parse.quote(query)}",
                "server3": f"https://autoembed.co/movie/tmdb/0?q={urllib.parse.quote(query)}"
            }

        # Fallback agar Torrent par na mile
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
