import os
import requests
from bs4 import BeautifulSoup

TOKEN_V3 = os.environ.get("TOKEN_V3")
DATABASE_ID = os.environ.get("DATABASE_ID")
LETTERBOXD_USERNAME = os.environ.get("LETTERBOXD_USERNAME")
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

def get_letterboxd_diary():
    url = f"https://letterboxd.com{LETTERBOXD_USERNAME}/rss/"
    response = requests.get(url)
    if response.status_code != 200:
        print("Error al leer Letterboxd")
        return []
    soup = BeautifulSoup(response.content, "xml")
    items = soup.find_all("item")
    diary = []
    for item in items:
        title = item.find("title").text
        link = item.find("link").text
        rating = item.find("letterboxd:memberRating")
        rating_text = rating.text if rating else ""
        rewatch = item.find("letterboxd:rewatch")
        rewatch_text = rewatch.text if rewatch else "false"
        watched_date = item.find("letterboxd:watchedDate")
        watched_date_text = watched_date.text if watched_date else ""
        diary.append({
            "title": title,
            "link": link,
            "rating": rating_text,
            "rewatch": rewatch_text,
            "date": watched_date_text
        })
    return diary

# Ejecución simple para Notion
diary = get_letterboxd_diary()
print(f"Se han encontrado {len(diary)} películas en tu diario reciente.")
