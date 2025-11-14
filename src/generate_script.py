# generate_script.py — Viral-Optimized Reel Script Generator

from openai import OpenAI
import yaml
import random
import os


def run(language="hindi", category="life_lessons"):
    print("🧠 Generating viral-optimized script...")

    # Load API Key
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    client = OpenAI(api_key=config.get("openai_api_key"))

    # ======================================================
    # VIRAL REEL FORMAT (core secret sauce)
    # ======================================================
    viral_format = """
Write a short, viral-style reel script in EXACTLY 5 lines.

The script MUST follow this structure:

Line 1 → Strong hook (shock/emotion/curiosity)
Line 2 → Relatable truth (viewer feels 'this is me')
Line 3 → Insight / Turning point
Line 4 → Deep punchline / wisdom
Line 5 → Final powerful end punch (stronger than Line 1)

Rules:
- Pure Hindi (Devanagari)
- Each line under 8–10 words
- No long sentences
- No paragraphs
- No stories
- Each line on a new line
- Must sound cinematic & emotional
- Designed for subtitles (punchy rhythm)
"""

    # ======================================================
    # CATEGORY THEMES
    # ======================================================
    if category == "life_lessons":
        topic = "Theme: struggle, discipline, success, self-growth."
    elif category == "finance":
        topic = "Theme: wealth building, money habits, savings, investment."
    elif category == "spiritual":
        topic = "Theme: karma, peace, Bhagavad Gita, faith, inner strength."
    else:
        topic = "Theme: general motivation and personal transformation."

    full_prompt = viral_format + "\n\n" + topic

    # ======================================================
    # CALL OPENAI
    # ======================================================
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You write viral Hindi motivational scripts like a top 1M-subscriber reel creator."
            },
            {
                "role": "user",
                "content": full_prompt
            }
        ]
    )

    script_text = response.choices[0].message.content.strip()

    # Save for debugging
    os.makedirs("data/output", exist_ok=True)
    with open("data/output/latest_script.txt", "w") as f:
        f.write(script_text)

    print("\n✨ Viral Script Generated:\n")
    print(script_text, "\n")

    return script_text
