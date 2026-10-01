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
    return {"status": "online", "message": "FlixTime Direct Hindi Scraper is Running!"}

@app.get("/find_hindi_movie")
def find_hindi_movie(title: str):
    try:
        query = title.strip()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        # DuckDuckGo se direct Hindi/Dual audio sites search karna
        search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query + ' dual audio hindi vegamovies hdhub4u')}"
        response = requests.get(search_url, headers=headers, timeout=10)
        
        direct_link = None
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('a', class_='result__url')
            
            for r in results:
                href = r.get('href', '')
                if any(domain in href for domain in ['vegamovies', 'hdhub4u', 'luxmovies', 'extramovies']):
                    target_page = href
                    # Inner page se direct video/hubcloud/pixeldrain link nikalna
                    page_res = requests.get(target_page, headers=headers, timeout=8)
                    if page_res.status_code == 200:
                        page_soup = BeautifulSoup(page_res.text, 'html.parser')
                        for a in page_soup.find_all('a', href=True):
                            link = a['href']
                            if any(x in link.lower() for x in ['hubcloud', 'pixeldrain', 'gofile', '.mkv', '.mp4']):
                                direct_link = link
                                break
                    if direct_link:
                        break

        # Agar direct link mil jaye
        if direct_link:
            return {
                "status": "success",
                "title": query,
                "server1": direct_link,
                "server2": f"https://vidsrc.to/embed/movie/{urllib.parse.quote(query)}",
                "server3": f"https://autoembed.co/movie/tmdb/0?q={urllib.parse.quote(query)}"
            }

        # Fallback agar direct link na mile
        return {
            "status": "success",
            "title": query,
            "server1": f"https://vidsrc.to/embed/movie/{urllib.parse.quote(query)}",
            "server2": f"https://autoembed.co/movie/tmdb/0?q={urllib.parse.quote(query)}",
            "server3": f"https://vidsrc.me/embed/movie/{urllib.parse.quote(query)}"
        }

    except Exception as e:
        return {
            "status": "success",
            "title": title,
            "server1": f"https://vidsrc.to/embed/movie/0",
            "server2": f"https://vidsrc.to/embed/movie/0",
            "server3": f"https://vidsrc.to/embed/movie/0"
                       }
        
