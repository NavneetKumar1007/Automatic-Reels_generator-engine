import whisper
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
from tqdm import tqdm

def generate_subtitles(audio_path, video_clip):
    print("💬 Generating cinematic Hindi subtitles (AI synced)...")

    # Load Whisper model (tiny/small recommended for speed)
    model = whisper.load_model("small")
    result = model.transcribe(audio_path, language="hi")

    subtitle_clips = []
    video_w, video_h = video_clip.size

    # Merge small pauses and smooth transitions
    merged_segments = []
    for segment in result["segments"]:
        text = segment["text"].strip()
        start = max(segment["start"] - 0.2, 0)
        end = segment["end"] + 0.5

        # Merge with previous if short gap
        if merged_segments and start - merged_segments[-1]["end"] < 0.8:
            merged_segments[-1]["text"] += " " + text
            merged_segments[-1]["end"] = end
        else:
            merged_segments.append({"text": text, "start": start, "end": end})

    for segment in tqdm(merged_segments, desc="🎞️ Rendering cinematic subtitles"):
        text = segment["text"].strip()
        start = segment["start"]
        end = segment["end"]

        # Background semi-transparent bar for readability
        bg_bar = (
            ColorClip(size=(video_w, 200), color=(0, 0, 0))
            .set_opacity(0.4)
            .set_start(start)
            .set_end(end)
            .set_position(("center", video_h - 250))
        )

        # Text styling with glow and fade
        txt_clip = (
            TextClip(
                txt=text,
                fontsize=72,
                font="Devanagari-Sangam-MN",  # macOS Hindi font
                color="white",
                stroke_color="black",
                stroke_width=3,
                method="caption",
                size=(video_w - 200, None),
                align="center",
            )
            .set_position(("center", video_h - 300))
            .set_start(start)
            .set_end(end)
            .fadein(0.3)
            .fadeout(0.3)
            .margin(bottom=30, opacity=0)
            .set_position(lambda t: ("center", video_h - 310 + (t % 0.5)))  # gentle float
        )

        subtitle_clips.extend([bg_bar, txt_clip])

    print(f"✅ {len(merged_segments)} subtitle segments styled and synced.")
    final_video = CompositeVideoClip([video_clip, *subtitle_clips])
    return final_video

