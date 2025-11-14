from moviepy.editor import (
    VideoFileClip,
    concatenate_videoclips,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
)
import os
from datetime import datetime
from src.subtitles import generate_subtitles  # AI-synced subtitles


def run(script_text, voice_path, clip_paths, title_text):
    if not clip_paths:
        raise RuntimeError("No video clips available to compose the final reel.")

    os.makedirs("data/output", exist_ok=True)

    print("🎬 Creating cinematic reel with CENTER subtitles + golden signature watermark...")

    # 🧩 Merge all clips
    video_clips = []
    for path in clip_paths:
        try:
            clip = VideoFileClip(path).resize(height=1080).set_fps(24)
            video_clips.append(clip)
        except Exception as e:
            print(f"⚠️ Skipping clip {path} due to: {e}")

    if not video_clips:
        raise RuntimeError("No valid video clips were loaded successfully.")

    final_clip = concatenate_videoclips(video_clips, method="compose")

    # 🎵 Add voice
    audio = AudioFileClip(voice_path)
    final_clip = final_clip.set_audio(audio).set_duration(audio.duration)

    # 💬 Generate Whisper subtitles
    print("💬 Generating AI-synced subtitles...")
    try:
        subtitled_video = generate_subtitles(voice_path, final_clip)
    except Exception as e:
        print(f"⚠️ Subtitle generation failed ({e}), using fallback center subtitles.")
        subtitle = (
            TextClip(
                txt=script_text,
                fontsize=84,  # bigger font
                font="Devanagari-Sangam-MN",
                color="white",
                stroke_color="black",
                stroke_width=6,
                method="caption",
                size=(1000, None),
                align="center",
            )
            .set_position(("center", "center"))  # 🎯 Center of reel
            .set_duration(audio.duration)
        )
        subtitled_video = CompositeVideoClip([final_clip, subtitle])

    # 🌟 Golden @ArthaurJeevan watermark (bottom-right)
    watermark = (
        TextClip(
            "@ArthaurJeevan",
            fontsize=56,
            font="Lobster-Regular",  # classic artistic brush font
            color="#FFD700",  # gold
            stroke_color="black",
            stroke_width=3,
        )
        .set_position(("right", "bottom"))
        .set_duration(audio.duration)
        .fadein(1)
        .fadeout(1)
    )

    # 🧡 Combine everything (video + subtitles + watermark)
    final = CompositeVideoClip([subtitled_video, watermark])

    # 🎞️ Save with timestamp name
    filename = f"data/output/final_reel_ArthaurJeevan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    print(f"📽️ Rendering final reel → {filename}")

    final.write_videofile(filename, fps=24, audio_codec="aac", threads=4, preset="medium")

    print(f"✅ Final cinematic reel saved: {filename}")
    return filename

