"""
Demo: Real photo folder intake.
Creates sample photo filenames and scans them.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from engine.engine import AssetLibrary
from engine.photo_intake import scan_folder, print_scan_summary
from engine.engine import VariationEngine


def create_sample_photos(folder: Path):
    """Create dummy photo files with realistic names for testing."""
    folder.mkdir(parents=True, exist_ok=True)
    sample_names = [
        "childhood_school_glasses.jpg",
        "old_look_2019_before.jpg",
        "current_editorial_face.jpg",
        "current_physique_pump.jpg",
        "campaign_2xu_fullbody.jpg",
        "bts_set_melbourne.jpg",
        "movement_walk_turn.mp4",
        "face_closeup_premium.jpg",
        "old_kid_london.jpg",
        "current_fashion_editorial.jpg",
    ]
    for name in sample_names:
        (folder / name).write_text("placeholder")  # dummy content
    print(f"Created {len(sample_names)} sample photo files in {folder}")


if __name__ == "__main__":
    sample_folder = Path("/workspace/artifacts/affz_trial_engine/data/sample_photos")
    create_sample_photos(sample_folder)

    library = AssetLibrary()
    print("\nScanning folder...")
    assets = scan_folder(str(sample_folder), library)
    print_scan_summary(assets)

    library.save()
    print("\nLibrary saved.")

    # Quick generation test
    engine = VariationEngine(library)
    print("\nRecommended templates:", engine.recommend_templates())
    vars = engine.generate_batch("transform_years", count=4)
    print(f"\nGenerated {len(vars)} variations from scanned assets.")
