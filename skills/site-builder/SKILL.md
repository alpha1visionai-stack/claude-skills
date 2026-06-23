---
name: site-builder
description: |
  Comprehensive website template finder and professional site generator. Use this
  skill whenever the user wants to: (1) build, create, or design a website,
  landing page, portfolio, SaaS page, or business site; (2) find templates or
  inspiration for web design; (3) generate HTML/CSS/JS code for a site;
  (4) restyle or redesign an existing page with professional aesthetics.
  Covers the full workflow: needs analysis → template selection → generation.
---

# site-builder – Website Template Finder & Generator

This skill combines two phases: **find the right approach** (template, style, structure) then **generate a production-grade website** using [frontend-design](../../frontend-design/SKILL.md) for professional aesthetics.

## Workflow Overview

```
User request
  → Phase 1: Analyze requirements
  → Phase 2: Find template/style direction (references/template-repos.md)
  → Phase 3: Generate with frontend-design skill
  → Phase 4: Polish & deliver
```

---

## Phase 1: Analyze Requirements

Ask the user or extract from context:

1. **Purpose** — Landing page? Portfolio? SaaS product page? Blog? Dashboard?
2. **Tone/Aesthetic** — Minimal, maximalist, organic, tech-forward, luxury, playful?
3. **Content** — What sections/pages are needed? (hero, features, pricing, contact, etc.)
4. **Technical constraints** — Any framework preference, or pure HTML/CSS/JS?
5. **Deadline** — Quick one-pager or full multi-page site?

If the user is unsure about the aesthetic, use the design principles in `references/design-principles.md` to guide them.

---

## Phase 2: Find Template Direction

Open `references/template-repos.md` and match the user's needs to the right template category:

- **Landing Page / SaaS** → MasuRii, Orbitly, TrinkUI
- **Agency / Portfolio** → TrinkUI Agency, Astro Rocket
- **Multi-Page / Business** → Riccoc SaaS Template
- **AI / ML Product** → TrinkUI AI/ML
- **Dashboard / Admin** → Horizon UI
- **Documentation** → Starlight, Docusaurus

For pure HTML/CSS/JS (framework-agnostic), use the boilerplate in `references/boilerplate.md` as the starting point.

Explain to the user WHY a particular direction fits their needs.

---

## Phase 3: Generate the Website

Use the **frontend-design** skill (already installed globally) to generate the actual website code. The frontend-design skill handles:

- Bold aesthetic direction (typography, color, layout)
- Production-grade HTML/CSS/JS or component code
- Animations, micro-interactions
- Responsive design

### Integration steps:

1. **Load frontend-design context** — reference its guidelines
2. **Set the aesthetic direction** based on Phase 1+2 analysis
3. **Generate the site** — use the boilerplate from `references/boilerplate.md` as the base structure
4. **Apply template-specific patterns** — borrow layout ideas from the matched template repo

### Output structure (always):

```
site/
├── index.html
├── css/
│   └── style.css
├── js/
│   └── main.js
└── assets/
    └── (images, fonts, icons)
```

For multi-page sites, add:
```
├── pages/
│   ├── about.html
│   ├── pricing.html
│   └── contact.html
```

---

## Phase 4: Polish & Deliver

Before delivering, verify:

- [ ] Responsive (mobile, tablet, desktop)
- [ ] Semantic HTML5 structure
- [ ] CSS custom properties for theming
- [ ] Smooth transitions/animations
- [ ] No placeholder content unless noted
- [ ] Lighthouse-friendly basics (meta tags, viewport, headings hierarchy)

Deliver as a complete, ready-to-run folder. Offer to:
- Add the template to a git repo
- Deploy it (GitHub Pages, Netlify, Vercel)
- Further customize sections

---

## Design Principles Reference

See `references/design-principles.md` for:
- Typography pairing guide
- Color palette strategies
- Layout composition patterns
- Animation philosophy

## Boilerplate Reference

See `references/boilerplate.md` for:
- HTML5 starter template with meta/SEO tags
- CSS reset + custom properties setup
- JavaScript module scaffolding
- Accessibility baseline

## Template Repository Reference

See `references/template-repos.md` for:
- Curated list of 10+ professional template repos
- Categorized by purpose and tech stack
- Key features and links