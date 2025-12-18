#!/usr/bin/env python3
"""
FASTR Workshop Validator

Checks your workshop setup for common issues before building:
- Config.py syntax and required fields
- All files in deck_order exist
- All {{variables}} have values defined
- All image paths resolve correctly

Usage:
    python3 tools/02_check_workshop.py              # Interactive mode
    python3 tools/02_check_workshop.py --workshop 2025-nigeria
═══════════════════════════════════════════════════════════════════════
"""

import os
import sys
import re
import argparse
import importlib.util
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# AUTO-DETECT AND USE VENV
# ═══════════════════════════════════════════════════════════════════════════════

def ensure_venv():
    """Re-execute with venv Python if not already in venv."""
    if sys.prefix != sys.base_prefix:
        return
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    for venv_name in ['.venv', 'venv']:
        venv_python = project_root / venv_name / 'bin' / 'python3'
        if venv_python.exists():
            os.execv(str(venv_python), [str(venv_python)] + sys.argv)

ensure_venv()

# Sessions defined in build script
SESSIONS = {
    'intro': ['01_background_rationale.md', '02_fastr_approach.md'],
    'extraction': ['03_data_extraction.md'],
    'dq_assessment': ['04a_data_quality_assessment.md'],
    'dq_adjustment': ['04b_data_adjustment.md'],
    'disruption': ['05_service_utilization.md'],
    'coverage': ['06_coverage_analysis.md'],
    'facility': ['07_facility_assessments.md'],
}

# Required config fields
REQUIRED_FIELDS = ['name', 'date', 'location']


def list_workshops(base_dir):
    """List all available workshop folders"""
    workshops_dir = os.path.join(base_dir, "workshops")
    workshops = []

    if os.path.exists(workshops_dir):
        for item in os.listdir(workshops_dir):
            item_path = os.path.join(workshops_dir, item)
            config_path = os.path.join(item_path, "config.py")
            if os.path.isdir(item_path) and os.path.exists(config_path):
                workshops.append(item)

    return sorted(workshops)


def prompt_for_workshop(base_dir):
    """Ask user which workshop to check"""
    workshops = list_workshops(base_dir)

    if not workshops:
        print("No workshops found in workshops/ folder")
        sys.exit(1)

    print("\nAvailable workshops:")
    for i, w in enumerate(workshops, 1):
        print(f"  {i}. {w}")

    while True:
        choice = input("\nWhich workshop to check? (number or name): ").strip()

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(workshops):
                return workshops[idx]
        elif choice in workshops:
            return choice

        print(f"Invalid choice. Enter 1-{len(workshops)} or workshop name.")


def load_config(workshop_id, base_dir):
    """Load workshop config.py"""
    config_path = os.path.join(base_dir, "workshops", workshop_id, "config.py")

    try:
        spec = importlib.util.spec_from_file_location("config", config_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.WORKSHOP_CONFIG, None
    except Exception as e:
        return None, str(e)


def find_variables_in_file(filepath):
    """Find all {{variable}} patterns in a file"""
    variables = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        # Find all {{VARIABLE}} patterns
        matches = re.findall(r'\{\{(\w+)\}\}', content)
        variables.update(matches)
    except:
        pass
    return variables


def find_images_in_file(filepath):
    """Find all image references in a markdown file"""
    images = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        # Remove HTML comments (they may contain commented-out images)
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        # Find ![alt](path) patterns
        # Handle paths that may contain parentheses by matching until image extension + )
        pattern = r'!\[[^\]]*\]\((.*?\.(?:png|jpg|jpeg|gif|svg|webp))\)'
        matches = re.findall(pattern, content, re.IGNORECASE)
        images.extend(matches)
    except:
        pass
    return images


def resolve_image_path(image_ref, source_file, workshop_dir, base_dir):
    """
    Resolve an image path and check if it exists.
    Returns (resolved_path, exists, is_override)
    """
    # Handle relative paths
    if image_ref.startswith('../'):
        # Relative to source file location
        source_dir = os.path.dirname(source_file)
        resolved = os.path.normpath(os.path.join(source_dir, image_ref))
    elif image_ref.startswith('/'):
        resolved = image_ref
    else:
        # Relative to workshop folder
        resolved = os.path.join(workshop_dir, image_ref)

    # Check if workshop has an override
    # Extract the assets/ relative part if present
    if 'assets/' in image_ref:
        assets_rel = image_ref.split('assets/', 1)[1] if 'assets/' in image_ref else None
        if assets_rel:
            workshop_override = os.path.join(workshop_dir, 'assets', assets_rel)
            if os.path.exists(workshop_override):
                return workshop_override, True, True

    exists = os.path.exists(resolved)
    return resolved, exists, False


def check_workshop(workshop_id, base_dir):
    """Run all checks on a workshop"""

    workshop_dir = os.path.join(base_dir, "workshops", workshop_id)
    core_content_dir = os.path.join(base_dir, "core_content")

    errors = []
    warnings = []
    info = []

    print(f"\nChecking workshop: {workshop_id}")
    print("=" * 60)

    # ═══════════════════════════════════════════════════════════════
    # CHECK 1: Config.py syntax and loading
    # ═══════════════════════════════════════════════════════════════
    print("\n1. Config file...")
    config, error = load_config(workshop_id, base_dir)

    if error:
        errors.append(f"Config.py syntax error: {error}")
        print(f"   ERROR: {error}")
        # Can't continue without valid config
        return errors, warnings, info

    print("   OK: config.py loads successfully")

    # ═══════════════════════════════════════════════════════════════
    # CHECK 2: Required fields
    # ═══════════════════════════════════════════════════════════════
    print("\n2. Required fields...")
    for field in REQUIRED_FIELDS:
        value = config.get(field, '')
        if not value or value.strip() == '':
            warnings.append(f"Required field '{field}' is empty")
            print(f"   WARNING: '{field}' is empty")
        elif 'EXAMPLE' in str(value).upper() or 'YOUR' in str(value).upper():
            warnings.append(f"Field '{field}' appears to have placeholder text: {value}")
            print(f"   WARNING: '{field}' has placeholder text")

    if not any(f"'{f}'" in str(w) for w in warnings for f in REQUIRED_FIELDS):
        print("   OK: All required fields populated")

    # ═══════════════════════════════════════════════════════════════
    # CHECK 3: Files in deck_order exist
    # ═══════════════════════════════════════════════════════════════
    print("\n3. Deck order files...")
    deck_order = config.get('deck_order', [])
    files_checked = 0
    files_ok = 0

    for item in deck_order:
        if item == 'agenda':
            # Agenda template
            agenda_path = os.path.join(base_dir, "templates", "agenda.md")
            if not os.path.exists(agenda_path):
                errors.append(f"Agenda template missing: templates/agenda.md")
            files_checked += 1
            files_ok += 1

        elif item.endswith('.md'):
            # Custom slide in workshop folder
            custom_path = os.path.join(workshop_dir, item)
            if not os.path.exists(custom_path):
                errors.append(f"Custom slide missing: {item}")
                print(f"   ERROR: {item} not found")
            else:
                files_ok += 1
            files_checked += 1

        elif item in SESSIONS:
            # Built-in session - check core content files
            for filename in SESSIONS[item]:
                filepath = os.path.join(core_content_dir, filename)
                if not os.path.exists(filepath):
                    errors.append(f"Core content missing: {filename}")
                else:
                    files_ok += 1
                files_checked += 1

    if files_ok == files_checked:
        print(f"   OK: All {files_checked} files found")
    else:
        print(f"   Found {files_ok}/{files_checked} files")

    # ═══════════════════════════════════════════════════════════════
    # CHECK 4: Variables have values
    # ═══════════════════════════════════════════════════════════════
    print("\n4. Variable definitions...")

    # Build set of available variables
    available_vars = set()

    # Standard variables from config
    standard_vars = ['WORKSHOP_ID', 'WORKSHOP_NAME', 'DATE', 'LOCATION',
                     'FACILITATORS', 'CONTACT_EMAIL', 'WEBSITE',
                     'TEA_TIME', 'LUNCH_TIME', 'AFTERNOON_TEA_TIME', 'DAY_START_TIME',
                     'TEA_RESUME_TIME', 'LUNCH_RESUME_TIME']
    available_vars.update(standard_vars)

    # Variables from country_data
    country_data = config.get('country_data', {})
    available_vars.update(country_data.keys())

    # Find all variables used in files
    used_vars = set()
    files_to_check = []

    # Custom slides
    for item in deck_order:
        if item.endswith('.md'):
            files_to_check.append(os.path.join(workshop_dir, item))
        elif item in SESSIONS:
            for filename in SESSIONS[item]:
                files_to_check.append(os.path.join(core_content_dir, filename))

    # Templates
    files_to_check.append(os.path.join(base_dir, "templates", "title_slide.md"))
    files_to_check.append(os.path.join(base_dir, "templates", "closing.md"))

    for filepath in files_to_check:
        if os.path.exists(filepath):
            used_vars.update(find_variables_in_file(filepath))

    # Find undefined variables
    undefined = used_vars - available_vars
    if undefined:
        for var in sorted(undefined):
            warnings.append(f"Variable '{{{{{var}}}}}' used but not defined")
            print(f"   WARNING: {{{{{var}}}}} not defined")
    else:
        print(f"   OK: All variables defined ({len(used_vars)} used, {len(country_data)} country-specific)")

    # ═══════════════════════════════════════════════════════════════
    # CHECK 5: Image paths resolve
    # ═══════════════════════════════════════════════════════════════
    print("\n5. Image paths...")

    all_images = []
    for filepath in files_to_check:
        if os.path.exists(filepath):
            images = find_images_in_file(filepath)
            for img in images:
                all_images.append((img, filepath))

    # Also check agenda.png
    agenda_img = config.get('agenda_image', 'agenda.png')
    agenda_path = os.path.join(workshop_dir, agenda_img)

    images_ok = 0
    images_missing = 0
    overrides_found = 0

    checked_paths = set()
    for img_ref, source_file in all_images:
        if img_ref in checked_paths:
            continue
        checked_paths.add(img_ref)

        resolved, exists, is_override = resolve_image_path(
            img_ref, source_file, workshop_dir, base_dir
        )

        if exists:
            images_ok += 1
            if is_override:
                overrides_found += 1
        else:
            images_missing += 1
            warnings.append(f"Image not found: {img_ref}")
            print(f"   WARNING: {img_ref}")

    # Check agenda image separately
    if os.path.exists(agenda_path):
        images_ok += 1
        info.append(f"Agenda image: {agenda_img}")
    else:
        warnings.append(f"Agenda image missing: {agenda_img}")
        print(f"   WARNING: {agenda_img} not found")

    if images_missing == 0:
        msg = f"   OK: All {images_ok} images found"
        if overrides_found > 0:
            msg += f" ({overrides_found} workshop overrides)"
        print(msg)

    # ═══════════════════════════════════════════════════════════════
    # CHECK 6: Workshop assets folder (for overrides)
    # ═══════════════════════════════════════════════════════════════
    print("\n6. Workshop assets...")

    workshop_assets = os.path.join(workshop_dir, "assets")
    if os.path.exists(workshop_assets):
        # Count files in workshop assets
        asset_count = 0
        for root, dirs, files in os.walk(workshop_assets):
            asset_count += len(files)
        info.append(f"Workshop has {asset_count} custom assets")
        print(f"   INFO: {asset_count} custom assets in workshop/assets/")
    else:
        print("   INFO: No workshop-specific assets (using defaults)")

    # ═══════════════════════════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════════════════════════
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    if errors:
        print(f"\n  ERRORS: {len(errors)}")
        for e in errors:
            print(f"    - {e}")

    if warnings:
        print(f"\n  WARNINGS: {len(warnings)}")
        for w in warnings:
            print(f"    - {w}")

    if not errors and not warnings:
        print("\n  All checks passed!")
        print(f"\n  Ready to build:")
        print(f"    python3 tools/03_build_deck.py --workshop {workshop_id}")
    elif not errors:
        print(f"\n  Workshop can be built (review warnings above)")
        print(f"    python3 tools/03_build_deck.py --workshop {workshop_id}")
    else:
        print(f"\n  Fix errors before building")

    print("")
    return errors, warnings, info


def main():
    # Determine base directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)

    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Validate FASTR workshop setup")
        parser.add_argument('--workshop', required=True, help='Workshop folder name')
        args = parser.parse_args()
        workshop_id = args.workshop
    else:
        workshop_id = prompt_for_workshop(base_dir)

    check_workshop(workshop_id, base_dir)


if __name__ == "__main__":
    main()
