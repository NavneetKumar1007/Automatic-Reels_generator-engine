from openai import OpenAI
import yaml
import random
import os

def run(language="hindi", category="life_lessons"):
    print("🧠 Generating script using AI...")

    # Load OpenAI key from config
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    openai_key = config.get("openai_api_key")
    client = OpenAI(api_key=openai_key)

    # Define category-based prompt style
    if category == "life_lessons":
        topics = [
            "Write a short and emotional Hindi speech (under 200 words) about patience, struggle, and success. Make it sound inspiring and natural.",
            "Write a 30-40 second Hindi motivational message about hard work and dreams. Keep tone natural like a storyteller.",
            "Write a short Hindi inspirational paragraph about how failure is part of success.",
            "Write a short Hindi life lesson quote with emotional impact and practical advice."
        ]
    elif category == "finance":
        topics = [
            "Write a short Hindi explanation about personal finance, investing, or saving habits in a motivational tone.",
            "Explain one powerful finance fact related to India in Hindi under 4 lines.",
            "Write a short motivational Hindi script about growing wealth slowly with consistency."
        ]
    elif category == "spiritual":
        topics = [
            "Write a peaceful, spiritual Hindi script about life, karma, and inner peace.",
            "Write a 30-second Hindi reflection on Lord Krishna’s teachings.",
            "Write an inspirational Hindi script based on Bhagavad Gita concepts of action and patience."
        ]
    else:
        topics = [
            "Write a short motivational Hindi script about never giving up in life.",
            "Write a 30-second Hindi quote about courage and success."
        ]

    prompt = random.choice(topics)

    # Build full instruction
    if language.lower() == "hindi":
        prompt = f"Write in pure Hindi (Devanagari script). {prompt}"
    else:
        prompt = f"Write in English. {prompt}"

    # Generate script using OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a creative Hindi motivational script writer."},
            {"role": "user", "content": prompt}
        ],
    )

    script_text = response.choices[0].message.content.strip()

    # Save the script text for record
    os.makedirs("data/output", exist_ok=True)
    with open("data/output/latest_script.txt", "w") as f:
        f.write(script_text)

    return script_text

