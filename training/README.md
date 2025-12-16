# FASTR Slide Builder Training Materials

This folder contains onboarding materials for new team members.

## Training Presentation

**File:** `onboarding-presentation.md`

**To view as slides:**

### Option 1: View in Codespaces (Recommended)
1. Open repository in Codespaces
2. Open `training/onboarding-presentation.md`
3. Press Cmd/Ctrl+K V to preview
4. Navigate with arrow keys

### Option 2: View HTML in Browser
```bash
# Open the pre-generated HTML file
open training/onboarding-presentation.html
```

### Option 3: Export to HTML (regenerate)
```bash
cd training
marp onboarding-presentation.md --html -o onboarding-presentation.html
open onboarding-presentation.html
```

### Option 4: Export to PDF
```bash
cd training
marp onboarding-presentation.md --theme-set ../fastr-theme.css --pdf
open onboarding-presentation.pdf
```

## What's Covered

- Three ways to contribute (no installation needed!)
- Live demo: GitHub web editor
- Live demo: GitHub Codespaces (RECOMMENDED)
- Building your first deck
- Converting to PDF (RECOMMENDED method)
- Quick markdown tips
- Where to get help

## For Trainers

Use this presentation to onboard new team members. Recommended approach:

1. Present slides 1-12 (overview + Codespaces demo)
2. Have everyone create a Codespace and follow along
3. Walk through building example deck together
4. Give practice exercise (slide 24)
5. Answer questions

**Duration:** ~30-45 minutes including hands-on practice

## Files in this Folder

- `README.md` - This file
- `onboarding-presentation.md` - Marp presentation source (edit this)
- `onboarding-presentation.html` - Standalone HTML version (generated)
- `screenshots/` - Directory for demo images (optional)
