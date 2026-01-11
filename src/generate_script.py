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
        topic = "जीवन, अनुशासन, धैर्य, आत्मविकास"
    elif category == "finance":
        topic = "धन, निवेश, बचत, आर्थिक अनुशासन"
    elif category == "spiritual":
        topic = "कर्म, शांति, विश्वास, आत्मबल"
    else:
        topic = "प्रेरणा और आत्मपरिवर्तन"

    # =========================
    # SINGLE PROMPT
    # =========================
    prompt = f"""
You are a 1M+ follower Hindi reel creator for Indian audience.

Create content in PURE Hindi (Devanagari).
Tone: calm, confident, informative, motivational.
Audience: Indian retail investors (beginner to intermediate).

Return ONLY valid JSON. No markdown. No explanations.

IMPORTANT COMPLIANCE:
- This is NOT investment advice.
- Give HIGH-LEVEL public information only.
- Mention reputed institutions where relevant.
- Avoid buy/sell words.

JSON FORMAT (STRICT):
{{
  "script": [
    "Line 1 – strong hook",
    "Line 2 – reality check",
    "Line 3 – financial insight",
    "Line 4 – long-term thinking",
    "Line 5 – calm motivational close"
  ],
  "financial_snapshot": {{
    "gold": "भारत में सोने की वर्तमान स्थिति और अगले 1 वर्ष का उच्च-स्तरीय दृष्टिकोण (JPMorgan / World Gold Council जैसे स्रोतों के अनुसार)",
    "silver": "चांदी की वर्तमान स्थिति और अगले 1 वर्ष का उच्च-स्तरीय दृष्टिकोण",
    "real_estate": "भारत में औसत रियल एस्टेट मूल्य और अगले 1 वर्ष का दृष्टिकोण",
    "nifty_50": "निफ्टी 50 का वर्तमान स्तर और अगले 1 वर्ष का उच्च-स्तरीय दृष्टिकोण"
  }},
  "caption": "2–3 शांत और सोचने पर मजबूर करने वाली पंक्तियाँ",
  "hashtags": [
    "#धन",
    "#निवेश",
    "#आर्थिकसमझ",
    "#भारत",
    "#ArthAurJeevan"
  ]
}}

RULES FOR SCRIPT:
- EXACTLY 5 lines
- Each line max 8–10 words
- No emojis
- No stories
- Reel duration friendly (10–15 sec)

RULES FOR CAPTION:
- Plain text only
- No '\\n' literals
- Informational, not advisory

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
                "content": "You generate compliant, high-retention Hindi financial reels."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    raw_output = response.choices[0].message.content.strip()

    # =========================
    # PARSE JSON
    # =========================
    try:
        content = json.loads(raw_output)
    except json.JSONDecodeError:
        raise RuntimeError("❌ Invalid JSON from model:\n\n" + raw_output)

    script_text = "\n".join(content["script"])
    financial_block = (
        f"सोना: {content['financial_snapshot']['gold']}\n"
        f"चांदी: {content['financial_snapshot']['silver']}\n"
        f"रियल एस्टेट: {content['financial_snapshot']['real_estate']}\n"
        f"निफ्टी 50: {content['financial_snapshot']['nifty_50']}"
    )

    caption = content["caption"].strip()
    hashtags = " ".join(content["hashtags"])

    final_caption = f"{caption}\n\n{financial_block}\n\n{hashtags}"

    # =========================
    # SAVE OUTPUTS
    # =========================
    os.makedirs("data/output", exist_ok=True)

    with open("data/output/latest_script.txt", "w", encoding="utf-8") as f:
        f.write(script_text)

    with open("data/output/latest_caption.txt", "w", encoding="utf-8") as f:
        f.write(final_caption)

    # =========================
    # LOG
    # =========================
    print("\n✨ Script:\n", script_text)
    print("\n📝 Caption:\n", final_caption)

    return {
        "script_text": script_text,
        "caption": final_caption
    }
