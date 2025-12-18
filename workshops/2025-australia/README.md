# FASTR Workshop - australia

**Location:** perth
**Date:** dec 19-30 2025
**Facilitators:** TBD

## Files

- `workshop.yaml` - Workshop configuration (modules, schedule, etc.)
- Custom slides to edit:
  - `objectives.md` - Workshop objectives
  - `country-overview.md` - Country context
  - `health-priorities.md` - Health priorities
  - `next-steps.md` - Action items

## Build Your Deck

```bash
# Optional: Check setup
python3 tools/02_check_workshop.py 2025-australia

# Build the deck
python3 tools/03_build_deck.py 2025-australia

# Convert to PowerPoint (optional)
python3 tools/04_convert_pptx.py 2025-australia
```

## Country Outputs

Add your FASTR platform outputs to `media/outputs/` to include them in slides.
