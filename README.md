# Affz Trial Engine

Modeling-specific Trial Reel generation system for @affz.20.

## Goal
Grow follower count with premium model + accessible guy-next-door content.
Systematically test high-performing formats via Instagram Trial Reels with controlled variations.

## Core Rules
- Always change **at least 2 variables** per new Trial Reel
- Brand guardrails: non-political, non-offensive, premium + approachable
- Learn from performance over time

## What's Built

### 1. Photo Intake
```bash
python demo_intake.py
```
Scans a folder, tags assets by filename heuristics.

### 2. FFmpeg Renderer
Renders variation specs into 9:16 MP4s (placeholder frames for now).
Output goes to `output/`.

### 3. Web UI
```bash
python web_ui.py
```
Open http://localhost:8080  
- Scan folder  
- Generate variations  
- See JSON results

### 4. Templates + Hooks
10 templates with expanded hook libraries in `templates/templates.py`.

### 5. Performance Logging
```python
from engine.performance import log_performance, get_winning_patterns
log_performance("variation_id", views=15000, follows=120, graduated=True)
print(get_winning_patterns())
```

## Quick Demo
```bash
cd /workspace/artifacts/affz_trial_engine
python demo.py
```

## Project Structure
```
affz_trial_engine/
├── models/data_models.py
├── templates/templates.py
├── engine/
│   ├── engine.py          # Library + VariationEngine
│   ├── photo_intake.py    # Folder scanning
│   ├── renderer.py        # FFmpeg rendering
│   └── performance.py     # Learning loop
├── data/                  # Library + performance JSON
├── output/                # Rendered reels
├── web_ui.py
├── demo.py
└── demo_intake.py
```

## Next Real-World Steps
- Point intake at your actual photo folder
- Add real AI vision tagging (GPT-4o / Claude vision)
- Add music tracks and real text overlays in renderer
- Connect Instagram Graph API for Trial Reel posting
- Feed real performance numbers back into the system
