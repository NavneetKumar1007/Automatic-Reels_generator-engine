# generate_script.py
# Viral-Optimized Reel Script + Caption Generator (SINGLE API CALL)

from openai import OpenAI
import yaml
import os
import json


def run(language="hindi", category="life_lessons"):
    print("🧠 Generating viral reel script + caption (single call)...")

    # =========================
    # LOAD CONFIG
    # =========================
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    client = OpenAI(api_key=config.get("openai_api_key"))

    # =========================
    # CATEGORY THEMES
    # =========================
    if category == "life_lessons":
        topic = "struggle, discipline, consistency, self-growth"
    elif category == "finance":
        topic = "money mindset, savings, investment, financial discipline"
    elif category == "spiritual":
        topic = "karma, peace, faith, inner strength"
    else:
        topic = "motivation and personal transformation"

    # =========================
    # SINGLE PROMPT (SCRIPT + CAPTION)
    # =========================
    prompt = f"""
You are a top 1M-subscriber Hindi motivational reel creator.

Create content in PURE Hindi (Devanagari).
Return ONLY valid JSON. No explanations.

JSON format (strict):
{{
  "script": [
    "Line 1 – strong emotional hook",
    "Line 2 – relatable truth",
    "Line 3 – insight or turning point",
    "Line 4 – deep wisdom punch",
    "Line 5 – final powerful ending"
  ],
  "caption": "2–3 short emotional lines that encourage reflection or sharing",
  "hashtags": [
    "#अनुशासन",
    "#सपने",
    "#संघर्ष",
    "#जीवन",
    "#ArthAurJeevan"
  ]
}}

Rules for SCRIPT:
- EXACTLY 5 lines
- Each line under 8–10 words
- No paragraphs
- No stories
- Cinematic & emotional

Rules for CAPTION:
- 2–3 short lines
- Must emotionally match the script
- No emojis
- Encourage save/share

Rules for HASHTAGS:
- 4–6 hashtags
- Must match category: {category}

Theme focus:
{topic}
"""

    # =========================
    # CALL OPENAI
    # =========================
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You generate high-retention Hindi reel content."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    raw_output = response.choices[0].message.content.strip()

    # =========================
    # PARSE JSON SAFELY
    # =========================
    try:
        content = json.loads(raw_output)
    except json.JSONDecodeError:
        raise RuntimeError("❌ Model did not return valid JSON.\n\n" + raw_output)

    script_lines = content["script"]
    caption_text = content["caption"]
    hashtags = " ".join(content["hashtags"])

    # Final outputs
    script_text = "\n".join(script_lines)
    final_caption = caption_text + "\n\n" + hashtags

    # =========================
    # SAVE FOR DEBUGGING
    # =========================
    os.makedirs("data/output", exist_ok=True)
    with open("data/output/latest_script.txt", "w", encoding="utf-8") as f:
        f.write(script_text)

    with open("data/output/latest_caption.txt", "w", encoding="utf-8") as f:
        f.write(final_caption)

    # =========================
    # LOG OUTPUT
    # =========================
    print("\n✨ Script:\n")
    print(script_text)

    print("\n📝 Caption:\n")
    print(final_caption)
    print()

    # =========================
    # RETURN VALUES
    # =========================
    return {
        "script_text": script_text,
        "caption": final_caption
    }
