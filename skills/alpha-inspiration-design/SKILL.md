---
name: alpha-inspiration-design
description: Use when building or styling web pages, components, or UI mockups that should follow the "Alpha Inspiration" look and feel (Professional, Maritime, Calm Blue tones).
---

# Alpha Inspiration Design Skill

This skill allows you to replicate the visual identity and structural patterns of Alpha Inspiration for new web projects.

## Visual Identity (Design Tokens)

### Colors
- **Dark Blue (Primary)**: `#10556f` - Used for headers, hero backgrounds, and primary buttons.
- **Light Blue (Accent)**: `#98daf2` - Used for background sections and highlights.
- **Accent Blue**: `#15779b` - Used for hover states and borders.
- **Link Blue**: `#1e458a` - Standard color for links and CTA buttons.
- **Dark Text**: `#2b2b2b` - Primary font color on light backgrounds.
- **Gray Text**: `#757575` - Secondary info and footer text.

### Typography
- **Primary Font**: `Open Sans`, sans-serif.
- **Headings**: Semi-bold to Bold, centered for impact in Hero sections.
- **Line Height**: `1.6` for optimal readability.

## Functional Patterns

1.  **Hero Section**: Full-width dark blue background (`--alpha-dark-blue`), white text, centered content with a clear CTA (`#1e458a`).
2.  **Section Alternation**: Use light sections (White) followed by accent sections (`--alpha-light-blue` with ~90% opacity).
3.  **Cards**: Subtle border (`#efefef`), 8px border-radius, 1.5rem padding. On hover: translate -5px and blue border transition.
4.  **Tone**: Professional, calming, transformation-oriented (#spreadingthejoyoftransformation).

## Implementation Example

When requested to build a page in this style, use the provided CSS variables:

```css
:root {
  --alpha-dark-blue: #10556f;
  --alpha-light-blue: #98daf2;
  --alpha-accent-blue: #15779b;
  --alpha-link-blue: #1e458a;
  --alpha-white: #ffffff;
  --alpha-dark-text: #2b2b2b;
}
```

## Resources
Reference `assets/template.html` for the structural scaffold.
