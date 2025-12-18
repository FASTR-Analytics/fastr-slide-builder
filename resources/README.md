# Shared Resources

This folder contains shared images and media used across all workshops.

## Structure

```
resources/
├── diagrams/          # Methodology figures (FASTR cycle, workflow diagrams)
├── default_outputs/   # Default FASTR platform outputs (sample charts)
└── logos/             # FASTR brand assets
```

## Usage in Methodology Docs

Reference from `methodology/` folder:
```markdown
![FASTR Cycle](../resources/diagrams/GFF-Rapid-Cycle-Analytics-Data-Use_Figure-1.svg)
![Default Output](../resources/default_outputs/Default_1._Proportion_of_outliers.png)
![Logo](../resources/logos/FASTR_Primary_01_FullName.png)
```

## Usage in Slides (core_content/)

After extraction, slides reference:
```markdown
![FASTR Cycle](../../resources/diagrams/GFF-Rapid-Cycle-Analytics-Data-Use_Figure-1.svg)
```

## Adding New Images

- **Methodology diagrams** → `diagrams/`
- **Sample FASTR outputs** → `default_outputs/`
- **Brand assets** → `logos/`
- **Country-specific** → `workshops/{workshop}/media/`
