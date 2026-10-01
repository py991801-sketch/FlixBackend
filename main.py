from fastapi import FastAPI
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

# Multi-Platform Sources jo Hollywood aur Bollywood Hindi dono ko target karenge
TARGET_PLATFORMS = [
    "vegamovies",
    "rogmovies",
    "extramovies",
    "katmovieshd"
]

def smart_scraper_fallback(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    for platform in TARGET_PLATFORMS:
        try:
            search_term = f"site:{platform}.* {query} hindi dual audio"
            duck_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote_plus(search_term)}"
            
            res = requests.get(duck_url, headers=headers, timeout=6)
            if res.status_code != 200:
                continue
                
            soup = BeautifulSoup(res.text, 'html.parser')
            target_urls = []
            for a in soup.select('.result__url'):
                link = a.get_text().strip()
                if link:
                    target_urls.append(link if link.startswith('http') else 'https://' + link)
            
            for movie_url in target_urls[:2]:
                try:
                    m_res = requests.get(movie_url, headers=headers, timeout=6)
                    m_soup = BeautifulSoup(m_res.text, 'html.parser')
                    page_text = m_soup.get_text().lower()
                    
                    if any(kw in page_text for kw in ['hindi', 'dual audio', 'multi audio', 'org audio']):
                        for a in m_soup.find_all('a', href=True):
                            href = a['href']
                            if 'vcloud.fit' in href or 'hubcloud' in href:
                                return href
                except:
                    continue
        except:
            continue
            
    return None

@app.get("/find_hindi_movie")
def find_hindi_movie(title: str):
    try:
        link = smart_scraper_fallback(title)
        
        if link:
            if "vcloud.fit" in link and "/e/" not in link:
                link = link.replace("vcloud.fit/", "vcloud.fit/e/")
            return {"status": "success", "link": link}
        else:
            return {
                "status": "maintenance",
                "message": "Servers par update chal raha hai ya movie uplabdh nahi hai. Kripya thodi der baad try karein!"
            }
            
    except Exception as e:
        return {
            "status": "maintenance",
            "message": "System auto-recovery mode mein hai. Jaldi hi theek ho jayega."
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
                                         
