# Live Demo Script

Use this script to demonstrate the FASTR Slide Builder live!

---

## Demo: Building a Workshop Deck

**What you'll show:** Complete process from folder to PDF in ~5 minutes

---

### Step 1: Show the Workshop Folder (30 seconds)

```bash
# Navigate to the workshop
cd ~/Desktop/fastr-slide-builder
ls workshops/2025-01-demo-country/
```

**Say:**
> "Here's our workshop folder for Demo Country. It contains:"
> - `config.py` - Workshop settings (dates, location, sections to include)
> - `custom-slides.md` - Country-specific content
> - That's it! Very simple."

---

### Step 2: Show the Config (1 minute)

```bash
# Open the config
cat workshops/2025-01-demo-country/config.py
```

**Say:**
> "The config file tells the system:"
> - Workshop name, date, location
> - Which core FASTR sections to include (we selected 6 out of 7)
> - Whether to include breaks, agenda, closing slides
> - Which custom slides to add
>
> "Everything is customizable with simple Python variables."

---

### Step 3: Build the Deck (30 seconds)

```bash
# Build the deck
python3 tools/build_deck.py --workshop 2025-01-demo-country
```

**Say:**
> "Now watch - one command assembles everything:"
> - Reads the config
> - Adds title slide with our workshop details
> - Includes the selected core FASTR sections
> - Adds our custom slides
> - Adds break slides and closing
>
> "Output is a single markdown file in outputs/ folder."

---

### Step 4: Show the Output (1 minute)

```bash
# Show what was created
ls outputs/2025-01-demo-country_deck.md

# Peek at the content
head -30 outputs/2025-01-demo-country_deck.md
```

**Say:**
> "The assembled markdown includes:"
> - Marp frontmatter for styling
> - Our title slide with all the variables filled in
> - All the content we selected
>
> "This is now ready to convert to a presentation format."

---

### Step 5: Convert to PDF (1 minute)

```bash
# Convert to PDF (RECOMMENDED)
marp outputs/2025-01-demo-country_deck.md --theme-set fastr-theme.css --pdf
```

**Say:**
> "Now we convert to PDF - this is the RECOMMENDED format because:"
> - Perfect FASTR styling (teal headers, proper fonts)
> - Consistent across all computers
> - No layout issues
> - Ready to present
>
> "PowerPoint is also possible but requires more manual work."

---

### Step 6: Open the PDF (30 seconds)

```bash
# Open the final PDF
open outputs/2025-01-demo-country_deck.pdf
```

**Say:**
> "And here's our final presentation!"
> - Title slide with workshop details
> - Core FASTR content
> - Custom Demo Country slides
> - Break slides
> - Closing with contact info
>
> "From folder to presentation in under 5 minutes!"

---

### Step 7: Show Editing (BONUS - 2 minutes)

**If time allows, show live editing:**

```bash
# Open custom slides
code workshops/2025-01-demo-country/custom-slides.md
```

**Do live:**
1. Add a new slide to custom-slides.md
2. Save
3. Rebuild: `python3 tools/build_deck.py --workshop 2025-01-demo-country`
4. Re-render: `marp outputs/2025-01-demo-country_deck.md --theme-set fastr-theme.css --pdf`
5. Open updated PDF

**Say:**
> "Need to make changes? Just edit the markdown, rebuild, and regenerate!"

---

## Alternative: Show in Codespaces (BONUS)

**If you want to show zero-installation workflow:**

1. Open GitHub repository
2. Click Code → Codespaces → Create codespace
3. Wait 2 minutes (explain what's happening)
4. Run the same commands in the browser-based terminal
5. Download the PDF

**Say:**
> "Your team can do this from ANY computer - even locked work laptops!"
> "No installation needed. Everything runs in the browser."

---

## Key Points to Emphasize

✅ **Simple:** Just config + custom slides
✅ **Fast:** 5 minutes from folder to PDF
✅ **Reusable:** Core content shared across workshops
✅ **Customizable:** Easy to add country-specific content
✅ **Consistent:** FASTR branding automatically applied
✅ **Accessible:** Works locally or in browser (Codespaces)

---

## Common Questions & Answers

**Q: Can I edit the core FASTR content?**
A: Yes! Core content is in `core_content/` folder. Any edits benefit all workshops.

**Q: What if I want PowerPoint instead of PDF?**
A: Use `python3 tools/convert_to_pptx.py outputs/deck.md` but be aware you may need to adjust fonts/layouts.

**Q: How do I add images?**
A: Put images in your workshop folder or `assets/`, reference with `![alt](path/to/image.png)`

**Q: Can multiple people work on this?**
A: Yes! Use git to collaborate. Always pull before editing, push after changes.

**Q: What if someone doesn't have Python/Node.js?**
A: Use GitHub Codespaces! Everything pre-installed in browser.

---

## End of Demo

**Wrap up with:**

> "That's it! From a simple folder structure to a professional FASTR presentation in minutes."
>
> "All documentation is in the `docs/` folder:"
> - Markdown guide - how to write slides
> - Building decks - detailed workflow
> - Codespaces workflow - how to save work
> - Local setup - installation if needed
>
> "Questions?"

---
