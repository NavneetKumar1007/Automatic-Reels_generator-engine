import os
import random
import yaml
import requests

PEXELS_API_URL = "https://api.pexels.com/videos/search"

def run(script_text, clip_count, category):
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    api_key = config.get("pexels_api_key")

    print(f"🎥 Downloading vertical clips from Pexels for category: {category}...")

    search_keywords = {
        "life_lessons": ["motivation", "focus", "sunrise", "mountain", "silhouette", "city street", "determination", "hope"],
        "finance": ["India finance", "BSE building", "stock market India", "rupee", "business team", "growth chart", "office skyline"],
        "spiritual": ["temple", "Varanasi ghat", "meditation", "Ganga aarti", "diya lights", "yoga", "sunset peace", "Himalayas"]
    }

    keywords = random.sample(search_keywords[category], k=min(len(search_keywords[category]), clip_count))

    headers = {"Authorization": api_key}
    os.makedirs("data/background_videos", exist_ok=True)
    downloaded_paths = []

    for keyword in keywords:
        params = {"query": keyword, "orientation": "portrait", "per_page": 1}
        response = requests.get(PEXELS_API_URL, headers=headers, params=params)

        if response.status_code != 200:
            continue

        data = response.json()
        videos = data.get("videos", [])
        if not videos:
            continue

        video_url = videos[0]["video_files"][0]["link"]
        file_path = f"data/background_videos/{keyword.replace(' ', '_')}_{random.randint(1000,9999)}.mp4"

        try:
            video_data = requests.get(video_url)
            with open(file_path, "wb") as f:
                f.write(video_data.content)
            print(f"✅ Downloaded clip: {file_path}")
            downloaded_paths.append(file_path)
        except:
            pass

    print(f"🎬 Total portrait clips downloaded: {len(downloaded_paths)}")
    return downloaded_paths

