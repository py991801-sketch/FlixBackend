from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    return {"message": "FlixBackend Single Server is Running Live!"}

@app.get("/find_hindi_movie")
def find_hindi_movie(title: str):
    query = title.strip()
    
    # Sabse purana aur reliable single server (Vidsrc)
    stream_link = f"https://vidsrc.to/embed/movie/{urllib.parse.quote(query)}"
    
    return {
        "status": "success",
        "title": query,
        "link": stream_link,
        "server1": stream_link  # Frontend break na ho isliye server1 me bhi yahi link bhej rahe hain
    }
    
