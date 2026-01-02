# src/split_script_into_scenes.py
# Split script text into visual scenes

def split_into_scenes(script_text, max_scenes=5):
    """
    Converts a script into scene-wise visual hints.
    Each scene becomes ONE image later.
    """

    # Split by lines and clean
    lines = [l.strip() for l in script_text.split("\n") if l.strip()]

    scenes = []

    for line in lines[:max_scenes]:
        scenes.append({
            "text": line,
            "visual_hint": line
        })

    return scenes

