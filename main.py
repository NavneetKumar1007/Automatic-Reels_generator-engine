import random
import os
import yaml
from datetime import datetime
from openai import OpenAI
from src import text_to_speech, download_video, compose_video


def main():
    print("\n🎬 Starting AI Reels Generator...")

    # Load config
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    openai_key = config.get("openai_api_key")

    client = OpenAI(api_key=openai_key)

    # 🎯 Random category
    categories = ["life_lessons", "finance", "spiritual"]
    selected_category = random.choice(categories)
    print(f"🧠 Selected Category: {selected_category.replace('_', ' ').title()}")

    # Define prompts for each category
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

    # Select a random prompt for that category
    prompt = random.choice(PROMPTS[selected_category])
    prompt = f"Write in pure Hindi (Devanagari script). {prompt}"

    # Generate Hindi script
    print("\n🧠 Generating Hindi script using OpenAI...\n")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a creative Hindi motivational and storytelling script writer."},
            {"role": "user", "content": prompt}
        ],
    )
    script_text = response.choices[0].message.content.strip()
    print("📜 Script Generated:\n")
    print(script_text)

    # Save script
    os.makedirs("data/output", exist_ok=True)
    with open("data/output/latest_script.txt", "w") as f:
        f.write(script_text)

    # 🎬 Generate video title
    print("\n🧠 Generating video title...")
    title_prompt = f"Suggest a short, powerful Hindi video title (under 8 words) for this script: {script_text}"
    title_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a Hindi YouTube title creator."},
            {"role": "user", "content": title_prompt}
        ],
    )
    title_text = title_response.choices[0].message.content.strip().replace('"', '')
    print(f"🎬 Suggested Video Title: {title_text}\n")

    # 🎤 Generate deep male voice with random intro
    voice_path = text_to_speech.run(script_text)

    # 🔊 Calculate duration for clips
    try:
        from mutagen.mp3 import MP3
        audio = MP3(voice_path)
        voice_duration = audio.info.length
        clip_count = max(3, int(voice_duration / 6))
        print(f"🎧 Voice duration: {voice_duration:.1f}s → using {clip_count} clips.\n")
    except Exception:
        clip_count = 6
        print("⚠️ Could not detect audio length, using 6 clips.\n")

    # 🎥 Download matching clips from Pexels (based on category)
    clip_paths = download_video.run(script_text, clip_count, selected_category)

    # 🎬 Compose final cinematic reel
    final_output = compose_video.run(script_text, voice_path, clip_paths, title_text)

    print(f"\n✅ Final cinematic reel created: {final_output}")
    print(f"🕒 Ready for review!\n")
    print(f"📘 Facebook Description Suggestion:\n👉 {title_text}\n\n#ArthAurJeevan #Motivation #HindiReel #LifeLessons")


if __name__ == "__main__":
    main()

