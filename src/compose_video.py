# compose_video.py
# Cinematic reel generator using AI images + motion + LOGO watermark

from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeVideoClip,
)
from moviepy.video.fx import all as vfx
import os
from datetime import datetime

# Output settings
OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
OUTPUT_FPS = 30

END_PADDING = 0.5  # seconds (soft ending)


# -------------------------
# Image → Motion
# -------------------------
def image_to_motion_clip(
    image_path,
    duration,
    zoom_factor=1.08,
):
    """
    Convert static image into cinematic slow-zoom clip.
    """

    clip = (
        ImageClip(image_path)
        .set_duration(duration)
        .resize(height=OUTPUT_HEIGHT)
        .fx(
            vfx.resize,
            lambda t: 1 + (zoom_factor - 1) * (t / duration)
        )
        .set_position("center")
        .set_fps(OUTPUT_FPS)
    )

    return clip


# -------------------------
# Main Composer
# -------------------------
def run(
    voice_path,
    image_paths,
    background_music_path=None,
    logo_path="assets/logo/logo.png",
):
    """
    image_paths: ordered images
    voice_path: TTS audio
    background_music_path: optional
    logo_path: brand watermark
    """

    if not image_paths:
        raise RuntimeError("No images provided for video composition.")

    print("🎬 Creating cinematic reel from images...")

    # -------------------------
    # Voice
    # -------------------------
    voice = AudioFileClip(voice_path)
    voice_duration = voice.duration

    per_scene_duration = voice_duration / len(image_paths)

    # -------------------------
    # Image motion clips
    # -------------------------
    clips = [
        image_to_motion_clip(img, per_scene_duration)
        for img in image_paths
    ]

    base_video = concatenate_videoclips(clips, method="compose")
    base_video = base_video.set_duration(voice_duration)

    # -------------------------
    # Clean voice audio
    # -------------------------
    voice_clean = (
        voice
        .audio_fadein(0.15)
        .audio_fadeout(0.15)
    )

    final_audio = voice_clean

    # -------------------------
    # Optional background music
    # -------------------------
    if background_music_path and os.path.exists(background_music_path):
        music = (
            AudioFileClip(background_music_path)
            .volumex(0.12)
            .set_duration(voice_duration + END_PADDING)
            .audio_fadein(1.0)
            .audio_fadeout(1.0)
        )

        final_audio = CompositeVideoClip([base_video]).audio.fx(
            vfx.audio_mix, music
        )

    base_video = base_video.set_audio(final_audio)

    # -------------------------
    # LOGO WATERMARK
    # -------------------------
    overlays = [base_video]

    if logo_path and os.path.exists(logo_path):
        logo = (
            ImageClip(logo_path)
            .set_duration(voice_duration + END_PADDING)
            .resize(width=int(OUTPUT_WIDTH * 0.18))  # SAME size
            .set_opacity(1.0)  # full clarity
            .set_position(("right", "bottom"))
            .margin(
                right=40,
                bottom=60,
                left=18,
                top=12,
                opacity=0.30,  # subtle backing
                color=(0, 0, 0)
            )
        )

        overlays.append(logo)

    final = CompositeVideoClip(overlays)
    final = final.set_duration(voice_duration + END_PADDING)

    # -------------------------
    # Output
    # -------------------------
    os.makedirs("data/output", exist_ok=True)
    filename = f"data/output/final_reel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

    print("➡ Saving:", filename)

    final.write_videofile(
        filename,
        fps=OUTPUT_FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="medium",
    )

    return filename
