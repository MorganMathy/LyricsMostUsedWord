from collections import Counter
import requests
from pprint import pprint
from bs4 import BeautifulSoup


def get_all_urls():
    page_number = 1
    links = []
    while True:
        url = f"https://genius.com/api/artists/694/songs?page={page_number}&sort=popularity"
        r = requests.get(url)

        if r.status_code == 200:
            print(f"Fetching page {page_number}")
            response = r.json().get("response", {})
            next_page = response.get("next_page")

            songs = response.get("songs")
            links.extend([song.get("url") for song in songs])

            page_number += 1
            if not next_page:
                print("No more pages")
                break
    return links


def extract_lyrics(url):
    print(f"Fetching lyrics {url}...")
    r = requests.get(url)
    if r.status_code != 200:
        print(f"Failed to retrieve lyrics from URL: {url}")
        return []
    soup = BeautifulSoup(r.content, "html.parser")
    lyrics_div = soup.find("div", class_="Lyrics__Container-sc-1ynbvzw-5 Dzxov")
    if not lyrics_div:
        print("Lyrics not found on the page.")
        return []
    words = []
    for sentence in lyrics_div.stripped_strings:
        sentence_words = [
            word.strip(",").strip(".").strip("?").strip("!").lower()
            for word in sentence.split()
            if len(word) > 5 and not word.startswith("[") and not word.endswith("]")
        ]
        words.extend(sentence_words)

    return words


def get_all_worlds():
    urls = get_all_urls()
    words = []
    for url in urls:
        lyrics = extract_lyrics(url=url)
        words.extend(lyrics)

    counter = Counter(words)
    most_common_words = counter.most_common(15)
    pprint(most_common_words)


get_all_worlds()
