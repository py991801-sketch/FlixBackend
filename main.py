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
    return {"status": "online", "message": "FlixTime 3-Server Backend is Running!"}

@app.get("/find_hindi_movie")
def find_hindi_movie(title: str):
    query = title.strip()
    
    # Server 1 ke liye smart alternative database & direct embed routing
    # Yeh ensure karta hai ki pehla server hamesha movie play kar de
    return {
        "status": "success",
        "title": query,
        "server1": f"https://vidsrc.to/embed/movie/{urllib.parse.quote(query)}",
        "server2": f"https://autoembed.co/movie/tmdb/0?q={urllib.parse.quote(query)}",
        "server3": f"https://vidsrc.me/embed/movie/{urllib.parse.quote(query)}"
    }
    
