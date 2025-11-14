# src/subtitles.py
import whisper
from moviepy.editor import TextClip, CompositeVideoClip
from moviepy.video.fx import all as vfx_all
from tqdm import tqdm
import os

# try to use a local fonts/ directory first, fallback to system font name
FONT_CANDIDATES = [
    "fonts/Mukta-Bold.ttf",    # recommended: place Mukta-Bold.ttf in project/fonts/
    "Mukta-Bold",              # system-installed font name
    "NotoSansDevanagari-Bold", # alternate
    "Devanagari-Sangam-MN"     # fallback (mac default)
]


def pick_font():
    for f in FONT_CANDIDATES:
        if os.path.exists(f):
            return f
    # if none exist as file, return first candidate as a font name (MoviePy will attempt to resolve)
    return FONT_CANDIDATES[1]


def _clip_safe_position(video_w, video_h, y_ratio=0.76):
    """
    Return x,y suitable for lower-third placement while staying above UI
    """
    return ("center", int(video_h * y_ratio))


def generate_subtitles(audio_path, video_clip):
    """
    Generate whisper transcription, build TextClip subtitles optimized for 1080x1920 mobile reels.
    - Single line whenever possible, wraps to 2 lines automatically.
    - Lower-third placement at ~76% height.
    - White text with thick black stroke for maximum legibility.
    """
    print("💬 Generating perfect Hindi subtitles (Ananya-style)...")
    model = whisper.load_model("small")
    result = model.transcribe(audio_path, language="hi")

    subtitle_clips = []
    video_w, video_h = video_clip.size
    font = pick_font()
    max_width = int(video_w * 0.8)  # 80% width as Ananya style

    segments = result.get("segments", [])

    for seg in tqdm(segments, desc="🎞 Rendering subtitles"):
        text = seg["text"].strip()
        if not text:
            continue

        start = max(seg.get("start", 0) - 0.05, 0)
        end = seg.get("end", start + 2)

        # Primary TextClip settings (big, bold, readable)
        sub = TextClip(
            txt=text,
            fontsize=88,                       # tuned for 1080x1920
            font=font,
            color="white",
            stroke_color="black",
            stroke_width=6,                    # bold stroke for phones
            method="caption",                  # automatic wrapping
            align="center",
            size=(max_width, None),            # force wrapping at 80% width
        ).set_start(start).set_end(end)

        # position lower-third with gentle fade
        x_pos, y_pos = _clip_safe_position(video_w, video_h, y_ratio=0.76)
        sub = sub.set_position((x_pos, y_pos)).crossfadein(0.12).crossfadeout(0.12)

        subtitle_clips.append(sub)

    print(f"✅ Added {len(subtitle_clips)} subtitle segments.")
    # Compose with original video_clip (subtitles over video)
    return CompositeVideoClip([video_clip, *subtitle_clips]).set_duration(video_clip.duration)

