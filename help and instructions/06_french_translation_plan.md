# Plan: French Translation & Multi-language Support

## Summary
Add French language support using:
- `mkdocs-static-i18n` plugin for methodology docs (language toggle)
- AI-assisted translation with human review
- French slides only for specific workshops (per-workshop config)

---

## Step 1: Install i18n Plugin

**File: `requirements.txt`**
```
mkdocs-static-i18n>=1.0.0
```

---

## Step 2: Configure MkDocs for i18n

**File: `methodology/mkdocs.yml`**

Add to plugins section:
```yaml
plugins:
  - i18n:
      docs_structure: suffix  # Uses .fr.md suffix
      fallback_to_default: true
      languages:
        - locale: en
          name: English
          default: true
          build: true
        - locale: fr
          name: Français
          build: true
  - strip-slides  # existing
  - search        # existing
  # ... rest of plugins
```

Update theme language handling:
```yaml
extra:
  alternate:
    - name: English
      link: /en/
      lang: en
    - name: Français
      link: /fr/
      lang: fr
```

---

## Step 3: Create French Translation Files

For each methodology file, create a `.fr.md` version:
```
methodology/
├── index.md                    # English
├── index.fr.md                 # French
├── executive_summary.md
├── executive_summary.fr.md
├── 00_introduction.md
├── 00_introduction.fr.md
└── ...
```

**Translation workflow:**
1. Use Claude to generate draft French translation
2. Human review for technical accuracy and terminology
3. Add translation status comment at top of file

---

## Step 4: Update Slide Build for Language Support

**File: `tools/02_build_deck.py`**

Add optional `--lang` parameter:
- Default: builds `deck.md` (English)
- With `--lang fr`: builds `deck.fr.md` if exists

**File: Workshop `config.yml`**
Add optional languages field:
```yaml
name: "2025-example"
languages: ["en", "fr"]  # Optional - defaults to ["en"]
```

---

## Step 5: Update npm Scripts

**File: `package.json`**
```json
"scripts": {
  "build": "python3 tools/02_build_deck.py",
  "build:fr": "python3 tools/02_build_deck.py --lang fr",
  "translate": "python3 tools/translate.py"  # Optional helper
}
```

---

## Files to Modify

| File | Change |
|------|--------|
| `requirements.txt` | Add `mkdocs-static-i18n` |
| `methodology/mkdocs.yml` | Add i18n plugin config |
| `tools/02_build_deck.py` | Add `--lang` parameter |
| `package.json` | Add French build script |

## New Files to Create

| File | Purpose |
|------|---------|
| `methodology/*.fr.md` | French translations (incremental) |
| `workshops/*/deck.fr.md` | French slides (specific workshops only) |

---

## Implementation Order

1. Install plugin and configure mkdocs.yml
2. Test with one translated file (e.g., executive_summary.fr.md)
3. Verify language toggle works
4. Update build script for slides
5. Translate remaining files incrementally
