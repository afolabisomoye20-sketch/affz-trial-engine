"""
Core engine for Affz Trial Engine.
Handles asset library, tagging, and variation generation.
"""

import random
from typing import List, Dict, Optional
from datetime import datetime
import json
from pathlib import Path

from models.data_models import Asset, AssetCategory, AssetType, Variation, Hook, Template
from templates.templates import get_all_templates, get_template_by_id


class AssetLibrary:
    """Manages the user's photo/video library with tagging."""

    def __init__(self):
        self.assets: Dict[str, Asset] = {}
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def add_asset(self, filename: str, path: str = "", asset_type: AssetType = AssetType.PHOTO,
                  categories: Optional[List[AssetCategory]] = None,
                  tags: Optional[List[str]] = None,
                  face_detected: bool = False,
                  physique_visible: bool = False,
                  is_childhood: bool = False,
                  quality_score: float = 0.8,
                  notes: str = "") -> Asset:
        """Add an asset (manual or from scan)."""
        asset = Asset(
            filename=filename,
            path=path or filename,
            asset_type=asset_type,
            face_detected=face_detected,
            physique_visible=physique_visible,
            is_childhood=is_childhood,
            quality_score=quality_score,
            usability_score=quality_score * 0.9,
            notes=notes,
        )
        if categories:
            for c in categories:
                asset.add_category(c)
        if tags:
            asset.tags.update(tags)
        if is_childhood:
            asset.add_category(AssetCategory.CHILDHOOD)
        if physique_visible:
            asset.add_category(AssetCategory.PHYSIQUE)

        self.assets[asset.id] = asset
        return asset

    def get_assets_by_category(self, category: AssetCategory, exclude_ids: Optional[set] = None) -> List[Asset]:
        exclude_ids = exclude_ids or set()
        return [
            a for a in self.assets.values()
            if category in a.categories and a.id not in exclude_ids and not a.excluded
        ]

    def get_best_assets(self, categories: List[AssetCategory], count: int = 5,
                        exclude_ids: Optional[set] = None) -> List[Asset]:
        """Get highest quality assets matching any of the categories."""
        candidates = []
        seen = set()
        for cat in categories:
            for a in self.get_assets_by_category(cat, exclude_ids):
                if a.id not in seen:
                    candidates.append(a)
                    seen.add(a.id)
        # Sort by quality + usability
        candidates.sort(key=lambda x: (x.quality_score + x.usability_score, x.favorite), reverse=True)
        return candidates[:count]

    def save(self):
        """Persist library to JSON."""
        data = {aid: a.to_dict() for aid, a in self.assets.items()}
        with open(self.data_dir / "library.json", "w") as f:
            json.dump(data, f, indent=2, default=str)

    def load(self):
        """Load library from JSON (basic)."""
        path = self.data_dir / "library.json"
        if path.exists():
            with open(path) as f:
                data = json.load(f)
            # Simple reconstruction for demo
            for aid, d in data.items():
                asset = Asset(id=aid, filename=d.get("filename", ""))
                asset.quality_score = d.get("quality_score", 0.8)
                asset.usability_score = d.get("usability_score", 0.7)
                asset.face_detected = d.get("face_detected", False)
                asset.physique_visible = d.get("physique_visible", False)
                asset.favorite = d.get("favorite", False)
                self.assets[aid] = asset


class VariationEngine:
    """Generates variations with controlled changes (≥2 variables)."""

    MUSIC_STYLES = ["trending_hiphop", "cinematic", "chill_rnb", "energetic", "minimal_piano", "trending_afrobeats"]
    TEXT_STYLES = ["bold_white", "minimal_black", "cinematic_serif", "modern_sans", "handwritten"]
    COLOR_GRADES = ["neutral", "warm", "cool", "high_contrast", "film_grain", "clean"]
    PACINGS = ["slow", "medium", "fast"]

    def __init__(self, library: AssetLibrary):
        self.library = library
        self.templates = {t.id: t for t in get_all_templates()}

    def generate_batch(self, template_id: str, count: int = 8, seed: Optional[int] = None) -> List[Variation]:
        """Generate a batch of variations for a template."""
        if seed is not None:
            random.seed(seed)

        template = self.templates.get(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")

        # Get candidate assets
        required_cats = template.required_categories
        preferred_cats = template.preferred_categories or required_cats
        all_cats = list(set(required_cats + preferred_cats))

        candidates = self.library.get_best_assets(all_cats, count=20)
        if len(candidates) < template.min_assets:
            # Fallback: use any high quality
            candidates = list(self.library.assets.values())[:20]

        variations = []
        used_combinations = set()

        for i in range(count):
            # Select assets
            num_assets = random.randint(template.min_assets, min(template.max_assets, len(candidates)))
            selected = random.sample(candidates, num_assets)
            asset_ids = [a.id for a in selected]

            # Must change at least 2 things
            changes = []
            variation = Variation(template_id=template_id, assets_used=asset_ids)

            # Always vary hook
            hook = random.choice(template.hooks)
            variation.hook = hook
            changes.append("hook")

            # Vary music
            variation.music_style = random.choice(self.MUSIC_STYLES)
            changes.append("music")

            # Additional variations
            if random.random() > 0.4:
                variation.text_style = random.choice(self.TEXT_STYLES)
                changes.append("text_style")

            if random.random() > 0.5:
                variation.color_grade = random.choice(self.COLOR_GRADES)
                changes.append("color_grade")

            if random.random() > 0.6:
                variation.pacing = random.choice(self.PACINGS)
                changes.append("pacing")

            # Order seed for photo sequence
            variation.order_seed = random.randint(1, 1000)
            if random.random() > 0.5:
                changes.append("order")

            # Cover
            variation.cover_asset_id = random.choice(asset_ids)

            variation.changes_made = list(set(changes))  # unique

            # Avoid exact duplicates
            combo_key = (tuple(sorted(asset_ids)), hook.text, variation.music_style)
            if combo_key in used_combinations:
                continue
            used_combinations.add(combo_key)

            variations.append(variation)

        return variations

    def recommend_templates(self) -> List[str]:
        """Recommend templates based on available assets (simple heuristic)."""
        has_childhood = any(a.is_childhood or AssetCategory.CHILDHOOD in a.categories
                           for a in self.library.assets.values())
        has_physique = any(a.physique_visible or AssetCategory.PHYSIQUE in a.categories
                          for a in self.library.assets.values())
        has_campaign = any(AssetCategory.CAMPAIGN in a.categories for a in self.library.assets.values())

        recs = ["transform_years", "photobooth_max", "never_model", "before_after"]
        if has_physique:
            recs.insert(0, "pump_check")
        if has_campaign:
            recs.append("campaign")
        return recs[:5]
