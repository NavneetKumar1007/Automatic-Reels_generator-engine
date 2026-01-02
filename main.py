# main.py
# AI Reel Generator – Image Motion Pipeline (OPTION 1)

import os
import random
import yaml

from src.generate_script import run as generate_script
from src.split_script_into_scenes import split_into_scenes
from src.generate_images import generate_images
from src.text_to_speech import run as generate_voice
from src.compose_video import run as compose_video
from src.upload_to_facebook import upload_reel_to_facebook


def main():
    print("\n🎬 Starting AI Reel Generator (Image + Motion Mode)...\n")

    # =========================
    # LOAD CONFIG
    # =========================
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    fb_page_id = config["facebook"]["page_id"]
    fb_page_token = config["facebook"]["page_access_token"]

    # =========================
    # SELECT CATEGORY
    # =========================
    categories = ["life_lessons", "finance", "spiritual"]
    category = random.choice(categories)

    print(f"🧠 Category: {category.replace('_', ' ').title()}")

    # =========================
    # ENSURE DATA DIRS
    # =========================
    os.makedirs("data/output", exist_ok=True)
    os.makedirs("data/images", exist_ok=True)
    os.makedirs("data/metadata", exist_ok=True)

    # =========================
    # GENERATE SCRIPT
    # =========================
    content = generate_script(category=category)
    script_text = content["script_text"]
    caption = content["caption"]

    with open("data/output/latest_script.txt", "w", encoding="utf-8") as f:
        f.write(script_text)

    # =========================
    # SPLIT SCRIPT INTO SCENES
    # =========================
    scenes = split_into_scenes(script_text, max_scenes=5)
    scene_texts = [s["visual_hint"] for s in scenes]

    print(f"🧩 Script split into {len(scene_texts)} scenes")

    # =========================
    # GENERATE / REUSE IMAGES
    # =========================
    image_paths = generate_images(
        scenes=scene_texts,
        category=category
    )

    if not image_paths:
        raise RuntimeError("❌ No images available for video composition.")

    # =========================
    # GENERATE VOICEOVER
    # =========================
    voice_path = generate_voice(script_text)

    # =========================
    # COMPOSE FINAL VIDEO
    # =========================
    final_video = compose_video(
        voice_path=voice_path,
        image_paths=image_paths,
        background_music_path="assets/music/soft_motivation.mp3"
    )

    print(f"🎉 Reel created successfully: {final_video}")

    # =========================
    # AUTO UPLOAD TO FACEBOOK
    # =========================

    print("🚀 Uploading reel to Facebook...\n")

    upload_reel_to_facebook(
        page_id=fb_page_id,
        page_access_token=fb_page_token,
        video_path=final_video,
        caption=caption
    )
    print("\n✅ Pipeline completed successfully.\n")


if __name__ == "__main__":
    main()
