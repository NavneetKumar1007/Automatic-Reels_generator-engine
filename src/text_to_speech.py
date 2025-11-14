# text_to_speech.py — clean version (no static intros)
import os
import random
import yaml
from openai import OpenAI

def run(script_text):
    # Load config
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    client = OpenAI(api_key=config.get("openai_api_key"))
    os.makedirs("data/output", exist_ok=True)

    # Save voice file with random name
    file_name = f"data/output/voice_{random.randint(10000, 99999)}.mp3"

    print("🎤 Generating AI voice from final script...")

    # Convert script_text directly to TTS
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=script_text
    )

    with open(file_name, "wb") as f:
        f.write(response.read())

    print(f"✅ Voice generated successfully → {file_name}")
    return file_name
