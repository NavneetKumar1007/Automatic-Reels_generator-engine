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
    # Define category-based prompt style
    if category == "life_lessons":
    	topics = [
        	"Write a short Hindi reel script (4–6 lines). Each line must be short, punchy and under 10 words. No long paragraphs. Tone: motivational & cinematic.",
        	"Write a crisp Hindi motivational reel script about struggle and success. Max 5 lines. Each line separate for subtitles.",
        	"Write a short Hindi life lesson for reels. 4–5 lines. No story, only punchy lines.",
    	]
    elif category == "finance":
    	topics = [
        	"Write a short Hindi finance reel script (max 4–6 lines). Each line 1 sentence, under 10–12 words. Keep it practical and motivational.",
        	"Write a powerful Hindi reel about Indian finance or money habits. Max 5 lines. No paragraphs.",
        	"Write a punchy Hindi reel script about wealth building. 4–6 short lines.",
   	 ]
    elif category == "spiritual":
    	topics = [
        	"Write a short spiritual Hindi reel script. Max 4–6 lines. Each line short & devotional.",
        	"Write a crisp Hindi spiritual message inspired by Bhagavad Gita. 4–5 lines only.",
        	"Write a short Hindi reel about inner peace and faith. Max 6 lines.",
    	]
    else:
    	topics = [
        	"Write a short and powerful Hindi motivational reel (max 5 lines). No stories.",
        	"Write a punchy Hindi reel script about never giving up. Each line short.",
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

