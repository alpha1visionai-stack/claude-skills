# Design Principles for Professional Websites

## Typography

### Font Pairing Strategy
Choose fonts that are distinctive and characterful. Avoid overused fonts (Inter, Roboto, Arial).

**Display + Body combinations:**
- **Editorial**: Fraunces (display) + DM Sans (body) — warm, magazine-like
- **Tech-forward**: Plus Jakarta Sans (display/body) — clean, modern
- **Luxury**: Cormorant Garamond (display) + Karla (body) — elegant contrast
- **Playful**: Space Grotesk (display) + Sora (body) — geometric, friendly
- **Minimal**: Cabinet Grotesk (display) + Satoshi (body) — sharp, refined

### Fluid Typography
```css
:root {
  --step-0: clamp(1rem, 0.96rem + 0.22vw, 1.125rem);
  --step-1: clamp(1.25rem, 1.16rem + 0.43vw, 1.5rem);
  --step-2: clamp(1.56rem, 1.41rem + 0.76vw, 2rem);
  --step-3: clamp(1.95rem, 1.71rem + 1.24vw, 2.66rem);
  --step-4: clamp(2.44rem, 2.05rem + 1.93vw, 3.55rem);
}
```

---

## Color

### Palette Structure
Use CSS custom properties for consistent theming:

```css
:root {
  /* Dominant (70%) — backgrounds, large areas */
  --color-bg: #0a0a0b;
  --color-surface: #141416;

  /* Text (20%) — readability */
  --color-text-primary: #f5f5f7;
  --color-text-secondary: #86868b;

  /* Accent (10%) — CTAs, highlights, interactive */
  --color-accent: #6c5ce7;
  --color-accent-hover: #a29bfe;

  /* Semantic */
  --color-success: #00b894;
  --color-warning: #fdcb6e;
  --color-error: #e17055;
}
```

### Strategies
- **Mono + Accent**: One bold accent color on neutral background — clean, professional
- **Duotone**: Two complementary colors — distinctive, memorable
- **Gradient mesh**: Subtle multi-color gradients for depth — modern, rich
- **Light-on-dark**: Default to dark mode, offer light toggle — 2026 standard

---

## Layout & Composition

### Bento Grid
Asymmetrical grid with varying cell sizes. Use CSS Grid:

```css
.bento-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}
.bento-item-wide { grid-column: span 2; }
.bento-item-tall { grid-row: span 2; }
```

### White Space
- Generous padding (at least 2rem on mobile, 4-6rem on desktop)
- Section spacing: 4-8rem between major sections
- Line height: 1.6-1.8 for body text

### Breakpoints
```css
/* Mobile-first */
:root {
  --content-max: 72rem;    /* 1152px */
  --content-narrow: 48rem;  /* 768px */
  --gutter: clamp(1rem, 5vw, 2rem);
}
```

---

## Animation Philosophy

### When to Animate
- **Page load**: Staggered fade-in of sections (100-200ms delay between each)
- **Scroll**: Reveal elements as they enter viewport
- **Hover**: Subtle transforms on interactive elements
- **Navigation**: Smooth scroll, active state transitions

### Implementation (CSS-only preferred)

```css
/* Scroll reveal */
.reveal {
  opacity: 0;
  transform: translateY(2rem);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Staggered children */
.stagger > *:nth-child(1) { transition-delay: 0ms; }
.stagger > *:nth-child(2) { transition-delay: 100ms; }
.stagger > *:nth-child(3) { transition-delay: 200ms; }
/* etc. */
```

### Micro-interactions
- Buttons: scale(1.02) on hover
- Cards: subtle lift with shadow deepening
- Links: underline slide-in on hover
- Loaders: geometric pattern animations

---

## Accessibility Baseline

- All interactive elements focusable and keyboard-navigable
- Color contrast ratio ≥ 4.5:1 for text
- Alt text on all images
- aria-labels on icon-only buttons
- prefers-reduced-motion support
- Semantic HTML5 landmarks (header, main, nav, section, footer)

---

## SEO Essentials

```html
<meta name="description" content="...">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:image" content="...">
<link rel="canonical" href="...">
```

Include structured data (JSON-LD) for:
- Organization
- Product (for SaaS)
- LocalBusiness
- FAQ