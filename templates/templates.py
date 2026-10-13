"""
Modeling-specific Trial Reel templates for Affz (@affz.20).
Focused on premium model + accessible guy-next-door on the journey.
"""

from models.data_models import Template, TemplateTier, AssetCategory, Hook


def get_all_templates() -> list[Template]:
    """Return all production templates."""
    templates = []

    # ========== TIER 1 ==========

    # 1. Transformation / X Years Later
    templates.append(Template(
        id="transform_years",
        name="X Years Later / Glow-Up",
        tier=TemplateTier.TIER_1,
        description="Childhood or old photo → current premium model look. High shareability.",
        required_categories=[AssetCategory.CHILDHOOD, AssetCategory.CURRENT_PREMIUM],
        preferred_categories=[AssetCategory.FACE_CLOSEUP, AssetCategory.FULL_BODY],
        min_assets=2,
        max_assets=4,
        hooks=[
            Hook("6 years later...", "bold", "nostalgic"),
            Hook("From South London to this.", "minimal", "motivational"),
            Hook("They didn't see this coming.", "confident", "assertive"),
            Hook("Same kid. Different chapter.", "minimal", "nostalgic"),
            Hook("Built different.", "bold", "confident"),
            Hook("The journey continues.", "minimal", "motivational"),
            Hook("Still the same dream.", "minimal", "nostalgic"),
            Hook("Consistency over time.", "bold", "motivational"),
        ],
        structure=["old/childhood", "current", "text overlay"],
        variation_points=["hook", "order", "text_style", "music", "cover"],
        brand_notes="Keep premium but human. Avoid arrogant tone."
    ))

    # 2. Photoboothmaxxing / Polaroidmaxxing
    templates.append(Template(
        id="photobooth_max",
        name="Photoboothmaxxing / Polaroidmaxxing",
        tier=TemplateTier.TIER_1,
        description="Sequential photobooth or polaroid frames with strong hooks.",
        required_categories=[AssetCategory.FACE_CLOSEUP],
        preferred_categories=[AssetCategory.CURRENT_PREMIUM, AssetCategory.OLD_LOOK],
        min_assets=3,
        max_assets=6,
        hooks=[
            Hook("Photoboothmaxxing", "bold", "fun"),
            Hook("Polaroidmaxxing", "bold", "fun"),
            Hook("Boothmaxxing", "minimal", "fun"),
            Hook("A moment for the camera.", "minimal", "confident"),
            Hook("Frame by frame.", "minimal", "fun"),
            Hook("One take, many faces.", "bold", "fun"),
        ],
        structure=["photo sequence", "text at end or throughout"],
        variation_points=["hook", "order", "music", "text_style", "number_of_photos"],
        brand_notes="Playful but still premium. Good for volume testing."
    ))

    # 3. You Will Never Model / Underdog
    templates.append(Template(
        id="never_model",
        name="You Will Never Model",
        tier=TemplateTier.TIER_1,
        description="Old photo or early look with underdog text contrasting current success.",
        required_categories=[AssetCategory.OLD_LOOK, AssetCategory.CURRENT_PREMIUM],
        preferred_categories=[AssetCategory.CHILDHOOD],
        min_assets=2,
        max_assets=3,
        hooks=[
            Hook("You will NEVER model", "bold", "assertive"),
            Hook("You could NEVER model", "bold", "assertive"),
            Hook("I wanna be a model when I grow up.", "minimal", "nostalgic"),
            Hook("They said I wouldn't make it.", "emotional", "motivational"),
        ],
        structure=["old photo with text", "current photo"],
        variation_points=["hook", "text_style", "music", "order"],
        brand_notes="Motivational, not bitter. Fits South London → Australia journey."
    ))

    # 4. Before / After Strong Hook
    templates.append(Template(
        id="before_after",
        name="Before / After",
        tier=TemplateTier.TIER_1,
        description="Clear visual contrast with sharp text hook.",
        required_categories=[AssetCategory.OLD_LOOK, AssetCategory.CURRENT_PREMIUM],
        min_assets=2,
        max_assets=3,
        hooks=[
            Hook("Before.", "minimal", "neutral"),
            Hook("After.", "bold", "confident"),
            Hook("The art of disappearing and coming back better.", "minimal", "motivational"),
            Hook("Domain expansion", "bold", "confident"),
        ],
        structure=["before", "after", "text"],
        variation_points=["hook", "order", "music", "text_style", "color_grade"],
        brand_notes="Clean and premium."
    ))

    # 5. Pump Check / Physique
    templates.append(Template(
        id="pump_check",
        name="Pump Check / Domain Expansion",
        tier=TemplateTier.TIER_1,
        description="Confident physique or face shots with short assertive text.",
        required_categories=[AssetCategory.PHYSIQUE],
        preferred_categories=[AssetCategory.FACE_CLOSEUP, AssetCategory.FULL_BODY],
        min_assets=1,
        max_assets=4,
        hooks=[
            Hook("Pump check:)", "minimal", "confident"),
            Hook("Domain expansion", "bold", "assertive"),
            Hook("Built from consistency.", "minimal", "motivational"),
            Hook("No shortcuts.", "bold", "confident"),
        ],
        structure=["physique sequence", "text"],
        variation_points=["hook", "music", "text_style", "pacing", "order"],
        brand_notes="Keep it premium model, not pure fitness influencer."
    ))

    # ========== TIER 2 ==========

    # 6. Movement / Walk & Turn
    templates.append(Template(
        id="movement",
        name="Walk & Turn",
        tier=TemplateTier.TIER_2,
        description="Short movement clips showing professionalism.",
        required_categories=[AssetCategory.MOVEMENT],
        preferred_categories=[AssetCategory.CURRENT_PREMIUM],
        min_assets=1,
        max_assets=3,
        hooks=[
            Hook("Movement.", "minimal", "confident"),
            Hook("On set.", "minimal", "neutral"),
        ],
        structure=["movement clip(s)"],
        variation_points=["music", "pacing", "text_style"],
        brand_notes="Shows bookable quality."
    ))

    # 7. Behind the Scenes
    templates.append(Template(
        id="bts",
        name="Behind the Scenes",
        tier=TemplateTier.TIER_2,
        description="Real moments from set or prep. Accessible side.",
        required_categories=[AssetCategory.BTS],
        min_assets=1,
        max_assets=4,
        hooks=[
            Hook("Behind the scenes.", "minimal", "fun"),
            Hook("The work behind the look.", "minimal", "motivational"),
        ],
        structure=["bts clips or photos"],
        variation_points=["hook", "music", "order"],
        brand_notes="Guy-next-door energy."
    ))

    # 8. Campaign Reveal
    templates.append(Template(
        id="campaign",
        name="Campaign Reveal",
        tier=TemplateTier.TIER_2,
        description="Strong stills or clips from real jobs.",
        required_categories=[AssetCategory.CAMPAIGN],
        min_assets=1,
        max_assets=3,
        hooks=[
            Hook("Campaign.", "minimal", "confident"),
            Hook("Grateful for the work.", "minimal", "motivational"),
        ],
        structure=["campaign assets"],
        variation_points=["hook", "music", "text_style"],
        brand_notes="Premium. Credit teams when possible."
    ))

    # 9. Digitals / Clean Polaroid
    templates.append(Template(
        id="digitals",
        name="Digitals / Clean Polaroid",
        tier=TemplateTier.TIER_2,
        description="Natural light digitals presented cleanly.",
        required_categories=[AssetCategory.FACE_CLOSEUP],
        preferred_categories=[AssetCategory.FULL_BODY],
        min_assets=2,
        max_assets=4,
        hooks=[
            Hook("Digitals.", "minimal", "neutral"),
            Hook("Raw.", "minimal", "confident"),
        ],
        structure=["digitial sequence"],
        variation_points=["order", "music", "text_style"],
        brand_notes="Bookable and clean."
    ))

    # 10. Expectation vs Reality
    templates.append(Template(
        id="exp_reality",
        name="Expectation vs Reality",
        tier=TemplateTier.TIER_2,
        description="What people think modeling is vs the real process.",
        required_categories=[AssetCategory.BTS, AssetCategory.CURRENT_PREMIUM],
        min_assets=2,
        max_assets=4,
        hooks=[
            Hook("Expectation vs Reality", "bold", "fun"),
            Hook("What they see vs the work.", "minimal", "motivational"),
        ],
        structure=["expectation", "reality"],
        variation_points=["hook", "order", "music"],
        brand_notes="Relatable and human."
    ))

    return templates


def get_template_by_id(template_id: str) -> Template | None:
    for t in get_all_templates():
        if t.id == template_id:
            return t
    return None
