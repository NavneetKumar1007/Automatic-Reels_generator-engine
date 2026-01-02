# generate_images.py
# Generate scene images using OpenAI Image API
# Style: Minimalist 2D / flat illustration (for cinematic motion later)

import os
import json
import hashlib
from datetime import datetime
from openai import OpenAI
import yaml
import base64

METADATA_PATH = "data/metadata/images.json"


# -------------------------
# Metadata utilities
# -------------------------
def load_metadata():
    if not os.path.exists(METADATA_PATH):
        return {}
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_metadata(metadata):
    os.makedirs(os.path.dirname(METADATA_PATH), exist_ok=True)
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


# -------------------------
# Emotion inference
# -------------------------
def infer_emotion(text, category=None):
    t = text.lower()

    # ---- Finance ----
    if category == "finance":
        if any(x in t for x in ["पैसा", "धन", "गरीबी", "कर्ज"]):
            return "financial_anxiety"
        if any(x in t for x in ["बचत", "निवेश", "योजना"]):
            return "financial_discipline"
        return "money_mindset"

    # ---- Spiritual ----
    if category == "spiritual":
        if any(x in t for x in ["शांति", "आस्था", "भगवान", "कर्म"]):
            return "peace"
        return "faith"

    # ---- Life Lessons ----
    if any(x in t for x in ["अनुशासन", "मेहनत"]):
        return "discipline"
    if any(x in t for x in ["थक", "मुश्किल", "संघर्ष"]):
        return "struggle"
    if any(x in t for x in ["सपने", "उठो", "भागो"]):
        return "aspiration"

    return "motivation"


# -------------------------
# Stable image ID generator
# -------------------------
def generate_image_id(scene_text, category, emotion):
    """
    Generate a stable semantic ID for an image.
    Prevents overwrites and enables reuse.
    """
    key = f"{category}|{emotion}|{scene_text}"
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]


# -------------------------
# Prompt builder
# -------------------------
def build_image_prompt(scene_text):
    """
    Convert a script line into a visual prompt.
    We intentionally do NOT include text-on-screen.
    """

    base_style = """
Minimalist 2D illustration.
Flat vector style.
Cinematic lighting.
High contrast.
Emotional and motivational mood.
Human silhouette only (no face details).
Clean background.
Vertical composition (9:16).
"""

    prompt = f"""
{base_style}
Scene idea (do not add text in image):
{scene_text}
"""

    return prompt.strip()


# -------------------------
# Main image generator
# -------------------------
def generate_images(scenes, category="life_lessons", output_dir="data/images"):
    """
    scenes: list of scene strings
    category: life_lessons / finance / spiritual
    returns: list of image paths (ordered)
    """

    # Load API key
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    client = OpenAI(api_key=config.get("openai_api_key"))

    # Ensure directories exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.dirname(METADATA_PATH), exist_ok=True)

    metadata = load_metadata()
    image_paths = []

    print(f"🖼 Generating {len(scenes)} images using OpenAI...\n")

    for idx, scene in enumerate(scenes, start=1):
        emotion = infer_emotion(scene, category=category)
        image_id = generate_image_id(scene, category, emotion)

        image_name = f"{category}_{emotion}_{image_id}.png"
        image_path = os.path.join(output_dir, image_name)

        # ----------------------------------
        # SAFE CACHE REUSE
        # ----------------------------------
        if (
            os.path.exists(image_path)
            and image_name in metadata
            and metadata[image_name].get("status") == "usable"
        ):
            print(f"♻️ Using cached image: {image_path}")
            image_paths.append(image_path)
            continue

        # Build prompt
        prompt = build_image_prompt(scene)

        print(f"🎨 Scene {idx} prompt:")
        print(prompt)
        print("-" * 50)

        # Generate image
        try:
            result = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size="1024x1536",
                quality="medium"
            )
        except Exception as e:
            print(f"⚠️ Image generation failed for scene {idx}: {e}")
            print("👉 Stopping further generation for this run.")
            break

        # Save image
        image_base64 = result.data[0].b64_json
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(image_base64))

        print(f"✅ Saved: {image_path}\n")
        image_paths.append(image_path)

        # ----------------------------------
        # AUTO-METADATA WRITE
        # ----------------------------------
        metadata[image_name] = {
            "category": category,
            "emotion": emotion,
            "script_line": scene,
            "style": "minimalist_2d",
            "status": "usable",
            "created_from": "openai",
            "created_at": datetime.now().strftime("%Y-%m-%d")
        }

        save_metadata(metadata)

    return image_paths
