"""
Demo script for Affz Trial Engine.
Shows library setup, template selection, and variation generation.
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from models.data_models import AssetCategory, AssetType
from engine.engine import AssetLibrary, VariationEngine
from templates.templates import get_all_templates


def demo():
    print("=" * 60)
    print("AFFZ TRIAL ENGINE — DEMO")
    print("=" * 60)

    # 1. Create library and add sample assets (simulating upload + AI scan)
    library = AssetLibrary()

    print("\n[1] Building sample asset library (simulating upload + tagging)...")

    # Childhood / old
    library.add_asset(
        "childhood_school_01.jpg",
        categories=[AssetCategory.CHILDHOOD, AssetCategory.OLD_LOOK, AssetCategory.FACE_CLOSEUP],
        face_detected=True, is_childhood=True, quality_score=0.85,
        notes="School photo, glasses, age ~8"
    )
    library.add_asset(
        "old_look_2019.jpg",
        categories=[AssetCategory.OLD_LOOK, AssetCategory.FULL_BODY],
        face_detected=True, is_childhood=False, quality_score=0.75,
        notes="Early modeling attempts"
    )

    # Current premium
    library.add_asset(
        "current_editorial_01.jpg",
        categories=[AssetCategory.CURRENT_PREMIUM, AssetCategory.FACE_CLOSEUP, AssetCategory.FULL_BODY],
        face_detected=True, quality_score=0.95,
        notes="Strong editorial, high fashion"
    )
    library.add_asset(
        "current_campaign_2xu.jpg",
        categories=[AssetCategory.CAMPAIGN, AssetCategory.CURRENT_PREMIUM, AssetCategory.FULL_BODY],
        face_detected=True, quality_score=0.92,
        notes="2XU campaign"
    )
    library.add_asset(
        "current_physique_01.jpg",
        categories=[AssetCategory.PHYSIQUE, AssetCategory.CURRENT_PREMIUM, AssetCategory.FULL_BODY],
        physique_visible=True, face_detected=True, quality_score=0.90,
        notes="Clean physique shot"
    )
    library.add_asset(
        "current_face_close.jpg",
        categories=[AssetCategory.FACE_CLOSEUP, AssetCategory.CURRENT_PREMIUM],
        face_detected=True, quality_score=0.93,
        notes="Strong face, good lighting"
    )

    # More for volume
    for i in range(3):
        library.add_asset(
            f"bts_{i+1}.jpg",
            categories=[AssetCategory.BTS],
            quality_score=0.7,
            notes="Behind the scenes"
        )
        library.add_asset(
            f"movement_{i+1}.mp4",
            asset_type=AssetType.VIDEO,
            categories=[AssetCategory.MOVEMENT, AssetCategory.CURRENT_PREMIUM],
            quality_score=0.8,
            notes="Walk or turn"
        )

    print(f"   → {len(library.assets)} assets loaded and tagged.")

    # 2. Show available templates
    print("\n[2] Available templates:")
    templates = get_all_templates()
    for t in templates:
        print(f"   • {t.id:20} | {t.tier.value:8} | {t.name}")

    # 3. Recommend and generate
    engine = VariationEngine(library)
    recs = engine.recommend_templates()
    print(f"\n[3] Recommended templates for current library: {recs}")

    # Generate batch for top template
    target_template = "transform_years"
    print(f"\n[4] Generating 10 variations for '{target_template}'...")
    variations = engine.generate_batch(target_template, count=10)

    print(f"\n   Generated {len(variations)} variations:\n")
    for i, v in enumerate(variations, 1):
        hook_text = v.hook.text if v.hook else "N/A"
        print(f"   {i:2}. ID: {v.id}")
        print(f"       Hook: {hook_text}")
        print(f"       Music: {v.music_style}")
        print(f"       Text style: {v.text_style or 'default'}")
        print(f"       Changes: {', '.join(v.changes_made)}")
        print(f"       Assets: {len(v.assets_used)}")
        print()

    # Save library
    library.save()
    print("[5] Library saved to data/library.json")

    # Output summary
    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("\nNext steps for real use:")
    print("  1. Replace sample assets with real photo paths")
    print("  2. Add real AI vision tagging (GPT-4o vision or similar)")
    print("  3. Connect FFmpeg pipeline to actually render the Reels")
    print("  4. Add Instagram Graph API for Trial Reel posting")
    print("\nThe variation engine already enforces ≥2 changes per reel.")


if __name__ == "__main__":
    demo()
