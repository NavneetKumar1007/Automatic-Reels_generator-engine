🎬 ArthAurJeevan – Automated AI Reel Generator

An end-to-end automated pipeline that generates, animates, brands, and uploads cinematic motivational reels using AI — fully hands-free.

Built for Hindi motivational, finance, and spiritual content, optimized for Reels / Shorts / Facebook videos.

✨ What this project does

✔️ Generates viral Hindi scripts (motivational / finance / spiritual)
✔️ Converts scripts into AI-generated 2D cinematic images
✔️ Adds motion (Ken Burns effect) to static images
✔️ Generates natural AI voiceover
✔️ Adds brand logo watermark
✔️ Uploads automatically to Facebook Page
✔️ Runs once every 3 days using cron
✔️ Safely cleans up local videos to save disk space

🧠 High-Level Pipeline
Script (AI)
   ↓
Scene Split
   ↓
AI Image Generation (cached + metadata)
   ↓
Cinematic Motion (MoviePy)
   ↓
Voiceover (TTS)
   ↓
Logo Branding
   ↓
Facebook Upload
   ↓
Local Cleanup

📁 Project Structure
ai_reels_generator/
│
├── main.py                         # Orchestrates entire pipeline
├── run_hourly_upload.sh            # Cron-safe runner (3-day guard)
├── README.md
├── .gitignore
│
├── src/
│   ├── generate_script.py          # Script + caption generation (single API call)
│   ├── split_script_into_scenes.py # Scene planning
│   ├── generate_images.py          # AI image generation + metadata
│   ├── compose_video.py            # Motion + logo + audio
│   ├── text_to_speech.py           # Voice generation
│   └── upload_to_facebook.py       # Facebook upload + status
│
├── assets/                         # Local-only (logo, music)
│   ├── logo/
│   └── music/
│
├── data/                           # Runtime-generated (gitignored)
│   ├── images/
│   ├── metadata/
│   └── output/
│
├── logs/                           # Cron & execution logs
└── venv/

⚙️ Requirements

Python 3.9+

macOS / Linux

ffmpeg installed

OpenAI API key

Facebook Page access token

🔑 Configuration

Create this file (DO NOT COMMIT IT):

config/config.yaml

Example
openai_api_key: "YOUR_OPENAI_API_KEY"

facebook:
  page_id: "YOUR_PAGE_ID"
  page_access_token: "YOUR_PAGE_ACCESS_TOKEN"

🚀 How to run manually
source venv/bin/activate
python3 main.py

⏱ Automated Upload (Cron)

The pipeline is designed to run once every 3 days, even if the system was previously off.

Cron entry
0 21 * * * /Users/navneetkumar/ai_reels_generator/run_hourly_upload.sh

Safety features

Prevents duplicate uploads

Runs on next wake if Mac was off

Logs every execution

Deletes local video only after successful upload

💾 Storage Management

✅ AI images are cached and reused

✅ Metadata stored in data/metadata/images.json

✅ Final MP4 is deleted after upload

❌ Runtime data is not committed to Git

💰 Cost Awareness

This pipeline is optimized for low cost:

Scripts & captions → very low

Voice generation → low

Image generation → main cost (cached intelligently)

Typical cost per reel depends on the number of images generated.

🧹 What is intentionally NOT included

❌ Subtitles (deprecated due to quality issues)

❌ Stock video downloads

❌ Heavy animations (kept minimal for performance)

🧠 Design Philosophy

Quality over quantity

Deterministic automation

Minimal moving parts

Safe cleanup

Production-grade scheduling

This is creator automation, not spam automation.

📌 Future Enhancements (optional)

Telegram / Slack upload notifications

Budget-aware execution

End-card CTA

Image reuse by emotion

Cloud deployment (EC2 / Oracle Free Tier)

📜 License

This project is for personal and educational use.
You are free to modify and extend it for your own content pipelines.

🙌 Author

Arth Aur Jeevan
Building meaningful content at the intersection of
💰 Finance | 🧠 Life Lessons | 🧘 Spiritual Balance