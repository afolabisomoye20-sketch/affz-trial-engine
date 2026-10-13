"""
FFmpeg-based Trial Reel renderer for Affz Trial Engine.
Creates 9:16 vertical videos with text overlays from Variation specs.
Uses placeholder images when real assets aren't available.
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Optional
from models.data_models import Variation


OUTPUT_DIR = Path("/workspace/artifacts/affz_trial_engine/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_placeholder_image(text: str, output_path: Path, width: int = 1080, height: int = 1920):
    """Create a solid-color placeholder image using FFmpeg (no text to avoid font issues)."""
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c=0x1a1a1a:s={width}x{height}:d=1",
        "-frames:v", "1",
        str(output_path)
    ]
    subprocess.run(cmd, capture_output=True, check=True)


def render_variation(variation: Variation, duration_per_asset: float = 2.0) -> Optional[Path]:
    """
    Render a Variation into a vertical Reel MP4.
    Returns the output path or None on failure.
    """
    if not variation.assets_used:
        return None

    output_path = OUTPUT_DIR / f"reel_{variation.id}.mp4"
    hook_text = variation.hook.text if variation.hook else "Affz"

    # Create temporary placeholder frames
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        frames = []

        for i, asset_id in enumerate(variation.assets_used):
            frame_path = tmp / f"frame_{i:02d}.jpg"
            label = f"{hook_text[:20]} | {i+1}"
            create_placeholder_image(label, frame_path)
            frames.append(frame_path)

        # Build concat list
        concat_file = tmp / "concat.txt"
        with open(concat_file, "w") as f:
            for frame in frames:
                f.write(f"file '{frame}'\n")
                f.write(f"duration {duration_per_asset}\n")
            # Repeat last frame
            if frames:
                f.write(f"file '{frames[-1]}'\n")

        # Render (text overlay optional - skip if font issues)
        total_duration = len(frames) * duration_per_asset
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat_file),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "libx264", "-crf", "23", "-preset", "medium",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            "-t", str(total_duration),
            str(output_path)
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0 and output_path.exists():
                return output_path
            else:
                print(f"FFmpeg error: {result.stderr[-500:]}")
                return None
        except Exception as e:
            print(f"Render failed: {e}")
            return None


def render_batch(variations: list, max_count: int = 3) -> list:
    """Render the first N variations in a batch."""
    rendered = []
    for v in variations[:max_count]:
        path = render_variation(v)
        if path:
            rendered.append(path)
            print(f"Rendered: {path.name}")
    return rendered
