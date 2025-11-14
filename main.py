# main.py — Reel Generator + Dynamic Hook + Viral Caption + Facebook Upload

import random
import os
import yaml
from datetime import datetime
from openai import OpenAI
from src import text_to_speech, download_video, compose_video
from src.upload_to_facebook import upload_reel_to_facebook


def main():
    print("\n🎬 Starting AI Reels Generator...\n")

    # =========================
    # LOAD CONFIG
    # =========================
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    openai_key = config.get("openai_api_key")
    fb_page_id = config["facebook"]["page_id"]
    fb_page_token = config["facebook"]["page_access_token"]

    client = OpenAI(api_key=openai_key)

    # =========================
    # SELECT CATEGORY
    # =========================
    categories = ["life_lessons", "finance", "spiritual"]
    selected_category = random.choice(categories)
    print(f"🧠 Selected Category: {selected_category.replace('_', ' ').title()}\n")

    PROMPTS = {
        "life_lessons": [
            "Write a 30-second Hindi motivational message about hard work, struggle, and dreams. Make it sound powerful.",
            "Write a short Hindi script about patience, effort, and success in life.",
            "Write a Hindi motivational quote with an example of a famous person.",
        ],
        "finance": [
            "Write a short Hindi script explaining the power of saving and investing in India.",
            "Explain a surprising fact about India's economy or stock market in Hindi.",
            "Write a motivational Hindi script about growing wealth slowly and wisely.",
        ],
        "spiritual": [
            "Write a short Hindi reflection on peace, karma, and Bhagavad Gita lessons.",
            "Write a calming Hindi message about life, destiny, and God.",
            "Write a Hindi script about how spirituality brings inner strength.",
        ]
    }

    # =========================
    # GENERATE MAIN SCRIPT
    # =========================
    prompt = random.choice(PROMPTS[selected_category])
    prompt = f"Write in pure Hindi (Devanagari script). {prompt}"

    print("🧠 Generating Hindi script...\n")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a creative Hindi motivational storyteller."},
            {"role": "user", "content": prompt}
        ],
    )

    script_text = response.choices[0].message.content.strip()
    print("📜 Script:\n", script_text, "\n")

    # Save script
    os.makedirs("data/output", exist_ok=True)
    with open("data/output/latest_script.txt", "w") as f:
        f.write(script_text)

    # =========================
    # GENERATE TITLE (short)
    # =========================
    print("🧠 Generating title...\n")
    title_prompt = f"Suggest a short, powerful Hindi video title (under 8 words) for this script: {script_text}"

    title_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You write viral Hindi reel titles."},
            {"role": "user", "content": title_prompt}
        ],
    )

    title_text = title_response.choices[0].message.content.strip().replace('"', '')
    print(f"🎬 Title: {title_text}\n")

    # =========================
    # GENERATE VIRAL HOOK
    # =========================
    print("🧠 Generating hook...\n")

    hook_prompt = f"""
Write a powerful 1-line hook in pure Hindi (Devanagari) to instantly grab attention for this script:

{script_text}

Rules:
- Under 10 words
- Emotional or curiosity-building
- Spoken directly to the viewer (आप / तुम)
- Must hook within 2 seconds
"""

    hook_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You write viral short-form hooks."},
            {"role": "user", "content": hook_prompt}
        ],
    )

    intro_line = hook_response.choices[0].message.content.strip()
    print("🎤 Hook:", intro_line, "\n")

    # Merge hook + script for TTS
    final_voice_script = f"{intro_line}\n{script_text}"

    # =========================
    # GENERATE VIRAL CAPTION
    # =========================
    print("🧠 Generating viral caption...\n")

    caption_prompt = f"""
Write a viral-style reel caption in pure Hindi (Devanagari)
for this script:

{script_text}

The caption must:
- Be 2–3 short lines
- Emotional + curiosity-building
- Encourage people to watch till the end
- Feel personal and deep
- Add 4–6 powerful hashtags
- Add brand tag: @ArthAurJeevan
"""

    caption_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You write viral Instagram/Facebook captions."},
            {"role": "user", "content": caption_prompt}
        ],
    )

    final_caption = caption_response.choices[0].message.content.strip()
    print("📝 Caption:\n", final_caption, "\n")

    # =========================
    # GENERATE VOICEOVER
    # =========================
    voice_path = text_to_speech.run(final_voice_script)

    # =========================
    # CLIP COUNT FROM AUDIO LENGTH
    # =========================
    try:
        from mutagen.mp3 import MP3
        audio = MP3(voice_path)
        voice_duration = audio.info.length
        clip_count = max(3, int(voice_duration / 6))
        print(f"🎧 Duration: {voice_duration:.1f}s → {clip_count} clips\n")
    except:
        clip_count = 6
        print("⚠️ Duration fail → using 6 clips\n")

    # =========================
    # FETCH VIDEO CLIPS
    # =========================
    clip_paths = download_video.run(script_text, clip_count, selected_category)

    # =========================
    # CREATE FINAL REEL
    # =========================
    final_output = compose_video.run(final_voice_script, voice_path, clip_paths, title_text)

    print(f"🎉 Final reel created: {final_output}\n")

    print("📘 Ready Caption:\n", final_caption, "\n")

    # =========================
    # AUTO UPLOAD TO FACEBOOK
    # =========================
    print("🚀 Uploading to Facebook Page...\n")
    upload_reel_to_facebook(
        page_id=fb_page_id,
        page_access_token=fb_page_token,
        video_path=final_output,
        caption=final_caption
    )


if __name__ == "__main__":
    main()

