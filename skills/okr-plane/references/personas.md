# Personas — NPE Projekt (Vollständige Definitionen)

## Menschliche Rollen

### 👤 Moritz „Mo" Ostwald — Business Lead
**Rolle:** Gesamt-Produktverantwortlicher, CEO, Marketing- & Sales-Stratege. Trägt finale Verantwortung für OKRs, B2B-Sales (Workshops) und Verlagsmarketing (Buch).
**Approver für:** BUCH Exposé, Verlagskontakt, Launch-Content, WS Pricing & Sales, NPEA Business-Entscheidungen (KR 2.4)
**Review-Gate (Phase 4):** Gibt Konzepte und Briefings zusammen mit Oliver frei.
**Eng mit:** Ki-Agent-Project-Manager, Ki-Agent-Marketing
**Plane-Label:** `👤 Mo`

### 👤 Oliver Herrmann — Domain Lead
**Rolle:** Chief Content Officer, Fachbuch-Hauptautor, Didaktik-Leiter. Verantwortet inhaltliche Richtigkeit, Buchstruktur, Workshop-Didaktik.
**Approver für:** BUCH Kapitel-Entwürfe (alle 11), WS Workshop-Design & Facilitator-Guide, fachliches Review aller Content-Outputs
**Review-Gate (Phase 4):** Gibt inhaltliche Briefings frei.
**Eng mit:** Ki-Agent-Content-Writer, Ki-Agent-Content-Research
**Plane-Label:** `👤 Oliver`

### 👤 Walter — Technical Lead (CTO)
**Rolle:** Leitender Softwareentwickler, System-Integrator. Verantwortet technischen Stack, Deployment, APIs, Local Agent Controller (LAC).
**Approver für:** Alle NPEA Feature-Issues (Phase 7 = Abnahme), Architektur-Entscheidungen
**Review-Gate (Phase 7):** Gibt Code-Implementierungen frei → erst dann darf Feature live gehen.
**Eng mit:** Ki-Agent-Developer, Ki-Agent-Architect
**Plane-Label:** `👤 Walter`

---

## KI-Agenten

### 🤖 Ki-Agent-Briefing-Writer
**Rolle:** Product Owner & Anforderungsanalytiker. Übersetzt Skizzen und Konzepte in strukturierte Initiative-Briefings.
**Einsatz:** NPEA Phase 1–3 (Sketch, Plan, Initiative Briefing). Schreibt Input für Walter und Ki-Agent-Developer.
**Input von:** Mo, Oliver
**Output an:** Walter, Ki-Agent-Developer
**Projekte:** NPEA (O2)

### 🤖 Ki-Agent-Content-Writer
**Rolle:** Fachbuch-Autor, Content Creator, Didaktiker. Schreibt wissenschaftlich präzise aber packend und lesbar.
**Einsatz:** BUCH Phase 1–3 + 5–6 (Kapitel-Entwürfe, Überarbeitung), WS Phase 1–3 + 5–6 (Slides, Workbooks, Facilitator-Guides)
**Input von:** Ki-Agent-Content-Research (Quellen), Mo & Oliver (Feedback)
**Projekte:** BUCH (O1), WS (O3)

### 🤖 Ki-Agent-Content-Research
**Rolle:** Wissenschaftlicher Researcher. Analysiert Studien, Fachliteratur, bio-physiologische Daten.
**Einsatz:** Frühe Phasen aller Content-Projekte; Faktencheck-Issues; Quellenlieferant für Content-Writer.
**Verbunden mit:** RAG-Wissensdatenbanken (Mistral-Embed, Qdrant)
**Projekte:** BUCH (O1) Faktencheck-KRs, NPEA (O2) Research-Issues (R1, R2)

### 🤖 Ki-Agent-Architect
**Rolle:** Systemarchitekt. Entwirft Datenbankschemata, API-Strukturen, Cloud-Infrastrukturen.
**Einsatz:** NPEA Phase 5 (Technical Specification). Gibt Architekturvorgaben an Ki-Agent-Developer.
**Nur in:** technischen Projekten (NPEA)
**Projekte:** NPEA (O2)

### 🤖 Ki-Agent-Developer
**Rolle:** Senior Full-Stack Developer (Python, TypeScript, SQL). Schreibt robusten Code, Tests, Dokumentation.
**Einsatz:** NPEA Phase 6 (Doing & Implementation). Startet erst wenn Phase 4 (Review-Briefing) auf Done.
**Input von:** Ki-Agent-Architect (Architektur), Walter (Vorgaben)
**Projekte:** NPEA (O2)

### 🤖 Ki-Agent-Marketing
**Rolle:** B2B-Sales- & Marketing-Experte. Konzipiert Funnels, Landingpage-Texte, Outreach-Konzepte.
**Einsatz:** WS Phase 5–6 (Sales Deck, Pricing-Kommunikation), BUCH Launch-Content (LinkedIn-Plan, Verlags-Anschreiben)
**Projekte:** WS (O3), BUCH (O1) KR 1.5

### 🤖 Ki-Agent-Project-Manager
**Rolle:** Operativer Projektmanager. Strukturiert Roadmaps, überwacht Fristen, erstellt Statusberichte.
**Einsatz:** Projektübergreifend; BUCH und WS Phase 1–3 wenn organisatorische Strukturierung nötig.
**Unterstützt:** Mo bei operativer Steuerung
**Projekte:** alle (O1–O4)

---

## Ressourcen-Zuteilung nach Phase und Projekt

| Projekt | Phase 1–3 | Phase 4 (Gate) | Phase 5–6 | Phase 7 (Gate) |
|---|---|---|---|---|
| **BUCH** (O1) | Content-Writer + Content-Research | Mo + Oliver | Content-Writer | Oliver (Inhalt), Mo (Verlag) |
| **NPEA** (O2) | Briefing-Writer | Mo + Oliver | Architect (Spec) + Developer (Code) | Walter |
| **WS** (O3) | Content-Writer + Project-Manager | Mo + Oliver | Content-Writer + Marketing | Oliver (Didaktik), Mo (Sales) |
| **WHOLE** (O4) | Project-Manager | Mo | Marketing + Content-Writer | Mo + Oliver |

## DACI-Regel

- **Driver:** Genau 1 KI-Agent (ausführend), manchmal Mo/Oliver/Walter direkt
- **Approver:** Genau 1 Mensch (nie delegierbar, nie ein Team)
- **Contributor:** Optional — wer Input liefert
- **Informed:** Wer bei Fertigstellung Ping bekommt

Bei NPEA: immer Walter als Approver für technische Features.
Bei BUCH: Oliver für Inhalt, Mo für Business/Verlag — nie beide gleichzeitig Approver (→ Mo entscheidet wer der Finale ist).
