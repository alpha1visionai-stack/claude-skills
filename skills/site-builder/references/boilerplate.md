# HTML/CSS/JS Boilerplate

Standard structure for all generated sites. Use this as the foundation.

## Directory Structure

```
site/
├── index.html
├── css/
│   ├── reset.css        # CSS reset + base styles
│   ├── tokens.css       # Design tokens (colors, fonts, spacing)
│   └── style.css        # Layout and component styles
├── js/
│   ├── main.js          # App entry point
│   ├── animations.js    # Scroll reveals, transitions
│   └── navigation.js    # Mobile menu, smooth scroll
└── assets/
    └── images/          # Optimized images
```

## HTML5 Starter

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="[page description]">
  <meta property="og:title" content="[page title]">
  <meta property="og:description" content="[og description]">
  <meta property="og:image" content="[og image URL]">
  <meta name="theme-color" content="[brand color]">
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">

  <!-- Fonts: Google Fonts or self-hosted -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[Display]:wght@400;700&family=[Body]:wght@400;500;600&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="/css/tokens.css">
  <link rel="stylesheet" href="/css/reset.css">
  <link rel="stylesheet" href="/css/style.css">

  <title>[Site Title]</title>
</head>
<body>
  <header>
    <nav>
      <a href="/" class="logo">[Logo]</a>
      <button class="mobile-toggle" aria-label="Menü öffnen">
        <span></span><span></span><span></span>
      </button>
      <ul class="nav-links">
        <li><a href="#features">Features</a></li>
        <li><a href="#pricing">Preise</a></li>
        <li><a href="#contact">Kontakt</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <section id="hero">
      <h1>[Headline]</h1>
      <p>[Subheadline]</p>
      <a href="#cta" class="btn btn-primary">[CTA]</a>
    </section>

    <section id="features">
      <!-- Feature cards -->
    </section>

    <section id="pricing">
      <!-- Pricing cards -->
    </section>

    <section id="contact">
      <!-- Contact form -->
    </section>
  </main>

  <footer>
    <p>&copy; 2026 [Company]. All rights reserved.</p>
  </footer>

  <script src="/js/main.js" type="module"></script>
</body>
</html>
```

## CSS Design Tokens (tokens.css)

```css
:root {
  /* Typography */
  --font-display: '[Display Font]', serif;
  --font-body: '[Body Font]', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Fluid type scale */
  --text-xs: clamp(0.75rem, 0.7rem + 0.22vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.8rem + 0.33vw, 1rem);
  --text-base: clamp(1rem, 0.92rem + 0.39vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1rem + 0.56vw, 1.375rem);
  --text-xl: clamp(1.25rem, 1.1rem + 0.67vw, 1.625rem);
  --text-2xl: clamp(1.5rem, 1.25rem + 1.11vw, 2.125rem);
  --text-3xl: clamp(1.875rem, 1.5rem + 1.67vw, 2.75rem);
  --text-4xl: clamp(2.25rem, 1.75rem + 2.22vw, 3.5rem);

  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;
  --space-xl: 4rem;
  --space-2xl: 8rem;

  /* Layout */
  --content-max: 72rem;
  --content-narrow: 48rem;
  --gutter: clamp(1rem, 5vw, 2rem);

  /* Radius */
  --radius-sm: 0.375rem;
  --radius-md: 0.75rem;
  --radius-lg: 1.5rem;
  --radius-full: 9999px;

  /* Transitions */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --duration-fast: 200ms;
  --duration-base: 400ms;
  --duration-slow: 800ms;
}
```

## CSS Reset (reset.css)

```css
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  scroll-behavior: smooth;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  font-family: var(--font-body);
  font-size: var(--text-base);
  line-height: 1.6;
  color: var(--color-text-primary);
  background-color: var(--color-bg);
  min-height: 100vh;
}

img, picture, video, canvas, svg {
  display: block;
  max-width: 100%;
}

input, button, textarea, select {
  font: inherit;
  color: inherit;
}

a { color: inherit; text-decoration: none; }
h1, h2, h3, h4 { font-family: var(--font-display); line-height: 1.2; }
ul { list-style: none; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## Scroll Animation Helper (animations.js)

```javascript
export function initScrollReveal() {
  const elements = document.querySelectorAll('.reveal');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

  elements.forEach(el => observer.observe(el));
}
```

## Navigation Helper (navigation.js)

```javascript
export function initNavigation() {
  const toggle = document.querySelector('.mobile-toggle');
  const nav = document.querySelector('.nav-links');

  toggle?.addEventListener('click', () => {
    nav?.classList.toggle('open');
    toggle.setAttribute('aria-expanded',
      toggle.getAttribute('aria-expanded') === 'true' ? 'false' : 'true');
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      e.preventDefault();
      const target = document.querySelector(anchor.getAttribute('href'));
      target?.scrollIntoView({ behavior: 'smooth' });
    });
  });
}
```

## Main Entry (main.js)

```javascript
import { initScrollReveal } from './animations.js';
import { initNavigation } from './navigation.js';

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initScrollReveal();
});
```

## Section Pattern: Feature Cards

```html
<section id="features" class="section">
  <div class="container">
    <h2 class="section-title reveal">[Section Title]</h2>
    <p class="section-subtitle reveal">[Section subtitle]</p>
    <div class="feature-grid">
      <article class="feature-card reveal">
        <div class="feature-icon">[icon]</div>
        <h3>[Feature Title]</h3>
        <p>[Feature description]</p>
      </article>
      <!-- Repeat for each feature -->
    </div>
  </div>
</section>
```

## Section Pattern: CTA

```html
<section class="cta-section">
  <div class="container">
    <h2 class="reveal">[CTA Headline]</h2>
    <p class="reveal">[CTA text]</p>
    <a href="#" class="btn btn-primary reveal">[Button Text]</a>
  </div>
</section>
```