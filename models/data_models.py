"""
Data models for the Affz Trial Engine.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum
from datetime import datetime
import uuid


class AssetType(Enum):
    PHOTO = "photo"
    VIDEO = "video"


class AssetCategory(Enum):
    CHILDHOOD = "childhood"
    OLD_LOOK = "old_look"
    CURRENT_PREMIUM = "current_premium"
    PHYSIQUE = "physique"
    MOVEMENT = "movement"
    BTS = "bts"
    CAMPAIGN = "campaign"
    FACE_CLOSEUP = "face_closeup"
    FULL_BODY = "full_body"
    OTHER = "other"


class TemplateTier(Enum):
    TIER_1 = "tier_1"
    TIER_2 = "tier_2"
    TIER_3 = "tier_3"


@dataclass
class Asset:
    """A photo or video in the user's library."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    filename: str = ""
    path: str = ""
    asset_type: AssetType = AssetType.PHOTO
    categories: Set[AssetCategory] = field(default_factory=set)
    tags: Set[str] = field(default_factory=set)
    quality_score: float = 0.0  # 0-1
    usability_score: float = 0.0  # 0-1, how usable for reels
    face_detected: bool = False
    physique_visible: bool = False
    is_childhood: bool = False
    is_current: bool = False
    uploaded_at: datetime = field(default_factory=datetime.utcnow)
    notes: str = ""
    # Manual overrides
    favorite: bool = False
    excluded: bool = False

    def add_category(self, cat: AssetCategory):
        self.categories.add(cat)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "filename": self.filename,
            "categories": [c.value for c in self.categories],
            "tags": list(self.tags),
            "quality_score": self.quality_score,
            "usability_score": self.usability_score,
            "face_detected": self.face_detected,
            "physique_visible": self.physique_visible,
            "is_childhood": self.is_childhood,
            "favorite": self.favorite,
        }


@dataclass
class Hook:
    """A text hook for a reel."""
    text: str
    style: str = "default"  # e.g. "bold", "minimal", "emotional", "confident"
    emotion: str = "neutral"  # e.g. "motivational", "nostalgic", "assertive", "fun"


@dataclass
class Template:
    """A Trial Reel template."""
    id: str
    name: str
    tier: TemplateTier
    description: str
    required_categories: List[AssetCategory]
    preferred_categories: List[AssetCategory] = field(default_factory=list)
    min_assets: int = 2
    max_assets: int = 6
    hooks: List[Hook] = field(default_factory=list)
    structure: List[str] = field(default_factory=list)  # e.g. ["childhood", "current", "text"]
    variation_points: List[str] = field(default_factory=list)
    brand_notes: str = ""


@dataclass
class Variation:
    """A specific generated variation of a template."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    template_id: str = ""
    assets_used: List[str] = field(default_factory=list)  # asset ids
    hook: Optional[Hook] = None
    music_style: str = ""
    text_style: str = ""
    order_seed: int = 0
    color_grade: str = "neutral"
    pacing: str = "medium"
    cover_asset_id: Optional[str] = None
    changes_made: List[str] = field(default_factory=list)  # what was varied
    generated_at: datetime = field(default_factory=datetime.utcnow)
    # Performance (filled later)
    views: Optional[int] = None
    retention: Optional[float] = None
    follows: Optional[int] = None
    graduated: bool = False

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "template_id": self.template_id,
            "assets_used": self.assets_used,
            "hook": self.hook.text if self.hook else None,
            "music_style": self.music_style,
            "text_style": self.text_style,
            "changes_made": self.changes_made,
            "color_grade": self.color_grade,
            "pacing": self.pacing,
        }
