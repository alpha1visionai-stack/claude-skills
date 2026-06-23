# NPE OKR-Struktur — Referenz

> **Hinweis:** Diese Datei wird nach jedem `/okr-add` Workflow 4 automatisch aktualisiert.
> Single Source of Truth für Sync-Konfiguration: `stacks/okr-sync-config.json`


## Objectives → Plane-Projekte

| Objective | Plane-Projekt | Typ |
|---|---|---|
| O1 — Buchmanuskript verlagsreif & eingereicht | `BUCH` | Konzeptionell |
| O2 — App & Tech: NPE Companion produktionsreif | `NPEA` | Technisch |
| O3 — Workshops: Tier-2-Pilot erfolgreich | `WS` | Konzeptionell |
| O4 — WholeVital GmbH operativ | `WHOLE` | Querschnitt (kein Task-Pool) |

## Key Results → Plane-Module

### O1 BUCH
| Modul | Name | Issues |
|---|---|---|
| KR 1.1 | Manuskript komplett | 11 Kap-Entwürfe + Schlaf-Playbook + Kap-3-Integration |
| KR 1.2 | Exposé fertig | OH1–25 abarbeiten, Zielgruppen-Analyse, Exposé USA |
| KR 1.3 | Faktencheck 100% grün | Schlaf-Plays validiert, Leitformel untermauert |
| KR 1.4 | ≥ 5 DACH-Verlage platziert | Top 5 DACH-Verlage kontaktiert |
| KR 1.5 | Launch-Vorbereitung | LinkedIn-Plan, Playbooks, Bits & Pretzels |

### O2 NPEA
| Modul | Name | Deadline-Anker |
|---|---|---|
| KR 2.1 | Radar als Buch-Funnel scharf | 04.10.2026 |
| KR 2.2 | Play-Library produktionsreif | erledigt (6 Done) |
| KR 2.3 | X-Ray entscheidungsreif | 25.10.2026 |
| KR 2.4 | Produkt-Roadmap-Entscheidung | MRT vs. WV Companion |

**KR 2.2 Stand:** Play-Taxonomie ✓ · One-Pager Template ✓ · MIND (15) ✓ · BODY (20) ✓ · CULTURE (15) ✓ · SYSTEMS (15) ✓

### O3 WS
| Modul | Name |
|---|---|
| KR 3.1 | Tier 2 komplett durchführbar |
| KR 3.2 | 1 zahlender Tier-2-Pilot |
| KR 3.3 | Pricing + Sales-Material |
| KR 3.4 | Tier 1 & 3 Grobkonzept |

## 7-Phasen-Pipeline (NPEA Features)

Jedes Feature = 1 Parent + 7 Subtasks (8 Issues gesamt):
```
Feature: [Name]
  1. Sketch & Concept: [Name]
  2. Project Plan & Timeline: [Name]
  3. Initiative Briefing: [Name]
  4. Review-Briefing: [Name]           ← GATE: Mo/Oliver müssen auf Done setzen
  5. Technical Specification: [Name]
  6. Doing & Implementation: [Name]
  7. Testing & final Review: [Name]    ← GATE: Walter muss abnehmen
```

## Aktive NPEA Features (KR 2.1 — Deadline Juli/Aug 2026)
- Feature: NPE Radar v2.0 (12.07.)
- Feature: UI Polish & Branding (12.07.)
- Feature: Email Capture & Provider Integration (02.08.)
- Feature: Deployment Pipelines (02.08.)
- Feature: QR-Code & URL-System (04.10.)
- Feature: Group Live-Dashboard (04.10.)

## Parkplatz-Features (🅿️ Future — kein Sprint)
- Feature: MRT Dashboard Design
- Feature: Wearable-Integration
- Feature: Team X-Ray Assessment
- Feature: Team Analytics Dashboard
+ 5 lose B2B/MRT-Issues
