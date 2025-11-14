import os
import random
import yaml
from openai import OpenAI

def run(script_text):
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    client = OpenAI(api_key=config.get("openai_api_key"))
    os.makedirs("data/output", exist_ok=True)

    # Random powerful intros
    intros = [
        "सुनिए ध्यान से, क्योंकि ये आपके लिए है।",
        "एक मिनट दीजिए, ये बात आपकी जिंदगी बदल देगी।",
        "ध्यान से सुनिए, ये शब्द आपकी सोच बदल सकते हैं।",
        "रुकिए ज़रा, ये कहानी आपके दिल को छू लेगी।",
        "एक पल ठहरिए, ये प्रेरणा आपके काम आएगी।"
    ]
    intro = random.choice(intros)
    print(f"🎬 Selected Intro: {intro}")

    full_script = f"{intro}\n\n{script_text}"

    # Generate voice
    file_name = f"data/output/voice_{random.randint(10000, 99999)}.mp3"
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=full_script
    )
    with open(file_name, "wb") as f:
        f.write(response.read())
    print(f"✅ Deep male Hindi voice generated successfully → {file_name}")
    return file_name

