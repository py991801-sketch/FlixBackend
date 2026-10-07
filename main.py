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
    return {"status": "online", "message": "FlixTime Hollywood Hindi API is Running!"}

@app.get("/find_hindi_movie")
def find_hindi_movie(title: str):
    try:
        query = title.strip()
        
        # APIBay se Hollywood movies ka Hindi dubbed/dual audio search
        search_query = urllib.parse.quote(f"{query} hindi")
        api_url = f"https://apibay.org/q.php?q={search_query}"
        response = requests.get(api_url, timeout=10)
        
        magnet_link = None
        if response.status_code == 200:
            data = response.json()
            
            # API se aaye saare results me se best Hindi Torrent find karna
            for torrent in data:
                if torrent.get("info_hash") != "0000000000000000000000000000000000000000":
                    name_lower = torrent["name"].lower()
                    # Sirf wohi torrent select karo jisme Hindi audio ho
                    if "hindi" in name_lower or "dual" in name_lower or "dub" in name_lower:
                        info_hash = torrent["info_hash"]
                        movie_name = torrent["name"]
                        magnet_link = f"magnet:?xt=urn:btih:{info_hash}&dn={urllib.parse.quote(movie_name)}"
                        break
                    
            # Agar specifically 'hindi' keyword ke sath naam na mile, toh pehla working link le lo
            if not magnet_link and len(data) > 0 and data[0].get("info_hash") != "0000000000000000000000000000000000000000":
                 info_hash = data[0]["info_hash"]
                 movie_name = data[0]["name"]
                 magnet_link = f"magnet:?xt=urn:btih:{info_hash}&dn={urllib.parse.quote(movie_name)}"

        # Magnet link milne par use seedha Webtor streaming player me bhej do
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
            
