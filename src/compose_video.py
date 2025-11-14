import cv2
import numpy as np
from moviepy.editor import (
    VideoFileClip,
    concatenate_videoclips,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
)
from moviepy.video.fx import all as vfx
import os
from datetime import datetime
from src.subtitles import generate_subtitles

OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
OUTPUT_FPS = 30


def _prepare_clip_for_vertical(clip):
    """
    Convert any clip (landscape/portrait/mixed) to perfect 1080x1920.
    """
    # Resize so height matches
    clip = clip.fx(vfx.resize, height=OUTPUT_HEIGHT)

    # If width is smaller than 1080, scale width
    if clip.w < OUTPUT_WIDTH:
        clip = clip.fx(vfx.resize, width=OUTPUT_WIDTH)

    # Center-crop exact 1080x1920
    clip = clip.fx(
        vfx.crop,
        width=OUTPUT_WIDTH,
        height=OUTPUT_HEIGHT,
        x_center=clip.w / 2,
        y_center=clip.h / 2,
    )

    return clip.set_fps(OUTPUT_FPS)


def _cv2_blur(image, blur_strength=35):
    """
    Gaussian blur via OpenCV (ALWAYS works on macOS).
    """
    return cv2.GaussianBlur(image, (blur_strength, blur_strength), 0)


def _stylize_background(clip):
    """
    Soft blur + dim background for crisp Ananya-style subtitles.
    """
    # Apply soft blur
    clip = clip.fl_image(lambda frame: _cv2_blur(frame, 35))

    # Dim slightly for readability
    clip = clip.fx(vfx.colorx, 0.85)

    return clip


def run(script_text, voice_path, clip_paths, title_text):
    if not clip_paths:
        raise RuntimeError("No video clips available.")

    print("🎬 Creating cinematic vertical reel (Ananya-style)...")

    processed = []

    for path in clip_paths:
        try:
            raw = VideoFileClip(path)
            v1 = _prepare_clip_for_vertical(raw)
            v2 = _stylize_background(v1)
            processed.append(v2)
        except Exception as e:
            print(f"⚠ Skipping {path}: {e}")

    if not processed:
        raise RuntimeError("No valid video clips loaded.")

    # Merge clips
    base = concatenate_videoclips(processed, method="compose")
    base = base.set_fps(OUTPUT_FPS).resize((OUTPUT_WIDTH, OUTPUT_HEIGHT))

    # Add audio
    audio = AudioFileClip(voice_path)
    base = base.set_audio(audio).set_duration(audio.duration)

    # Subtitles
    try:
        subtitled = generate_subtitles(voice_path, base)
    except Exception as e:
        print("⚠ Subtitle generation failed:", e)
        fallback = TextClip(
            txt=script_text,
            fontsize=70,
            color="white",
            stroke_color="black",
            stroke_width=3,
            method="caption",
            align="center",
            size=(int(OUTPUT_WIDTH * 0.8), None),
        ).set_position(("center", int(OUTPUT_HEIGHT * 0.76))).set_duration(
            audio.duration
        )
        subtitled = CompositeVideoClip([base, fallback])

    # Watermark (fully visible, right-aligned)
    watermark = (
        TextClip(
            "@ArthAurJeevan",
            fontsize=36,
            color="white",
            stroke_color="black",
            stroke_width=1,
        )
        .set_duration(audio.duration)
        .set_position(("right", "bottom"))   # right aligned
        .margin(right=40, bottom=60, opacity=0)   # SAFE margins
        .fadein(0.5)
    )

    final = CompositeVideoClip([subtitled, watermark]).set_duration(audio.duration)

    # Filename
    filename = f"data/output/final_reel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    print("➡ Saving:", filename)

    final.write_videofile(
        filename,
        fps=OUTPUT_FPS,
        audio_codec="aac",
        threads=4,
        preset="medium",
    )

    return filename

