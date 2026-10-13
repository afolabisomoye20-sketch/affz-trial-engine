"""
Photo intake and smart tagging for Affz Trial Engine.
Scans a folder of photos/videos and assigns categories using filename heuristics
(ready for real AI vision later).
"""

import os
from pathlib import Path
from typing import List, Optional
from models.data_models import Asset, AssetCategory, AssetType
from engine.engine import AssetLibrary


# Filename keyword → category mapping
KEYWORD_MAP = {
    "child": AssetCategory.CHILDHOOD,
    "kid": AssetCategory.CHILDHOOD,
    "young": AssetCategory.CHILDHOOD,
    "school": AssetCategory.CHILDHOOD,
    "old": AssetCategory.OLD_LOOK,
    "before": AssetCategory.OLD_LOOK,
    "early": AssetCategory.OLD_LOOK,
    "physique": AssetCategory.PHYSIQUE,
    "body": AssetCategory.PHYSIQUE,
    "pump": AssetCategory.PHYSIQUE,
    "gym": AssetCategory.PHYSIQUE,
    "campaign": AssetCategory.CAMPAIGN,
    "2xu": AssetCategory.CAMPAIGN,
    "rodd": AssetCategory.CAMPAIGN,
    "bts": AssetCategory.BTS,
    "behind": AssetCategory.BTS,
    "set": AssetCategory.BTS,
    "walk": AssetCategory.MOVEMENT,
    "turn": AssetCategory.MOVEMENT,
    "movement": AssetCategory.MOVEMENT,
    "face": AssetCategory.FACE_CLOSEUP,
    "close": AssetCategory.FACE_CLOSEUP,
    "editorial": AssetCategory.CURRENT_PREMIUM,
    "fashion": AssetCategory.CURRENT_PREMIUM,
    "premium": AssetCategory.CURRENT_PREMIUM,
    "model": AssetCategory.CURRENT_PREMIUM,
}


def infer_categories(filename: str) -> List[AssetCategory]:
    """Infer categories from filename keywords."""
    name = filename.lower()
    cats = set()
    for keyword, category in KEYWORD_MAP.items():
        if keyword in name:
            cats.add(category)
    # Defaults
    if not cats:
        cats.add(AssetCategory.CURRENT_PREMIUM)
    if "face" in name or "close" in name or "head" in name:
        cats.add(AssetCategory.FACE_CLOSEUP)
    return list(cats)


def scan_folder(folder_path: str, library: AssetLibrary) -> List[Asset]:
    """
    Scan a folder for images/videos and add them to the library with inferred tags.
    Supports .jpg, .jpeg, .png, .webp, .mp4, .mov
    """
    path = Path(folder_path)
    if not path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    extensions = {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov"}
    added = []

    for file in path.iterdir():
        if file.suffix.lower() not in extensions:
            continue

        asset_type = AssetType.VIDEO if file.suffix.lower() in {".mp4", ".mov"} else AssetType.PHOTO
        categories = infer_categories(file.name)

        # Simple quality heuristic
        quality = 0.85
        if "bts" in file.name.lower() or "behind" in file.name.lower():
            quality = 0.7
        if "child" in file.name.lower() or "old" in file.name.lower():
            quality = 0.75

        asset = library.add_asset(
            filename=file.name,
            path=str(file),
            asset_type=asset_type,
            categories=categories,
            face_detected=True,  # Assume for demo; real AI would detect
            physique_visible=AssetCategory.PHYSIQUE in categories,
            is_childhood=AssetCategory.CHILDHOOD in categories,
            quality_score=quality,
            notes=f"Scanned from {folder_path}"
        )
        added.append(asset)

    return added


def print_scan_summary(assets: List[Asset]):
    """Print a summary of scanned assets."""
    print(f"\nScanned {len(assets)} assets:")
    by_cat = {}
    for a in assets:
        for c in a.categories:
            by_cat.setdefault(c.value, []).append(a.filename)
    for cat, files in sorted(by_cat.items()):
        print(f"  {cat}: {len(files)} files")
        for f in files[:3]:
            print(f"    - {f}")
        if len(files) > 3:
            print(f"    ... and {len(files)-3} more")
