---
name: fast-detect-gpt
description: Hybrid KI-Texterkennung (Fast-DetectGPT Wahrscheinlichkeitskrümmung auf GPU + Stilometrie/AI-Slop + Burstiness & Struktur). Analysiert Text oder Dateien (.pdf, .md, .txt) objektiv auf KI-Echtheit und speichert strukturierte Markdown-Berichte (.md) mit Fundstellennachweis ab. Verwenden, wenn der Benutzer sagt oder andeutet: "bitte prüfe den text auf KI generierung", "prüfe auf KI", "ist dieser Text von einer KI geschrieben?", "KI-Check", "KI Text Detektor", "prüfe Datei auf KI", "KI Erkennung" oder ähnliche Aufforderungen zur KI-Texterkennung.
---

# Fast-DetectGPT Hybrid — AI Text Detector Skill

Dieser Skill analysiert übergebene Texte oder Dateien (PDF, Markdown, Textdateien, Aufsätze, Hausarbeiten, Blogbeiträge, Quelltexte) anhand eines **3-Säulen-Hybridmodells**:

1. **Mathematische Wahrscheinlichkeitskrümmung** (*Fast-DetectGPT, Bao et al. ICLR 2024* auf lokaler GPU)
2. **Stilometrische AI-Slop & Phrasen-Analyse** (Erkennung typischer Füllwörter, Einleitungsfloskeln & Buzzwords)
3. **Statistische Burstiness & Struktur-Metriken** (Satzlängen-Varianz $CV = \sigma / \mu$ & Listen-Dichte)

---

## ⚙️ Die 3 Säulen der Hybrid-Analyse

```
                  ┌────────────────────────────────────────────────────────┐
                  │              HYBRID KI-BEWERTUNG (100 %)               │
                  └──────────────────────────┬─────────────────────────────┘
                                             │
         ┌───────────────────────────────────┼──────────────────────────────────┐
         ▼ (60 %)                            ▼ (25 %)                           ▼ (15 %)
┌──────────────────────────┐       ┌──────────────────────────┐       ┌──────────────────────────┐
│ 1. MATHEMATIK            │       │ 2. STILOMETRIE (SLOP)    │       │ 3. STRUKTUR & BURSTINESS │
├──────────────────────────┤       ├──────────────────────────┤       ├──────────────────────────┤
│ • Wahrscheinlichkeits-   │       │ • Einleitungsfloskeln    │       │ • Satzrhythmus-Varianz   │
│   krümmung (Curvature)   │       │ • Stereotype Konnektoren │       │   ($CV = \sigma / \mu$)  │
│ • Log-Likelihood Ratio   │       │ • KI-Lieblings-Buzzwords │       │ • Listen- & Bullet-Ratio │
│ • Zero-Shot GPU-Inferenz │       │ • Fundstellen mit Zeilen │       │ • Absatz-Symmetrie       │
└──────────────────────────┘       └──────────────────────────┘       └──────────────────────────┘
```

* **Gesamtscore $\ge$ 75 %**: 🔴 **Sehr wahrscheinlich KI-generiert** (Monotoner Rhythmus, hohe Slop-Dichte, hohe Vorhersehbarkeit).
* **Gesamtscore 40 % – 75 %**: 🟡 **Gemischt / Teilweise KI-unterstützt** (Menschlicher Text mit KI-Politur oder stark formalisierte Fachsprache).
* **Gesamtscore < 40 %**: 🟢 **Sehr wahrscheinlich menschlich** (Hohe natürliche Satzrhythmus-Varianz $CV \ge 0.55$, organische Wortwahl).

---

## 🛠️ Ausführungspfade & Befehle

Die lokale Fast-DetectGPT-Installation befindet sich unter:
`D:\OneDrive\Development\fast-detect-gpt`

### 1. Bei direkt im Chat eingefügtem Text (Copy & Paste):
Führe das Python-Tool direkt über `uv run` auf der GPU aus:

```bash
uv run --directory "D:\OneDrive\Development\fast-detect-gpt" python detect_text.py --text "<Hier steht der zu prüfende Text>" --device cuda
```
> **Automatischer Speicherort:** Wird automatisch als `.md`-Bericht in das Verzeichnis `./dokumente/` des Projektordners geschrieben (z. B. `dokumente/ki_analyse_YYYYMMDD_HHMMSS_<snippet>.md`) und **enthält den vollständigen analysierten Originaltext**.

### 2. Bei Dateien (.pdf, .txt, .md):
Übergib den Dateipfad mit dem `--file` Parameter:

```bash
uv run --directory "D:\OneDrive\Development\fast-detect-gpt" python detect_text.py --file "<Dateipfad>" --device cuda
```
> **Automatischer Speicherort:** Wird automatisch als `.md`-Bericht im **selben Verzeichnis wie die Quelldatei** abgelegt (z. B. `<verzeichnis>/<dateiname>_ki_analyse.md`).

---

## 📋 Antwortformat für den Benutzer

Fasse das Ergebnis nach der Ausführung für den Benutzer in folgender klarer Struktur zusammen und verlinke immer den erzeugten Bericht:

1. **📊 1. Hybrid-Gesamtergebnis & Kernmetriken:**
   * **🎯 Gesamteinstufung (Hybrid):** z. B. `🟢 Sehr wahrscheinlich menschlich verfasst (17.9 %)`
   * **1. Fast-DetectGPT Curvature:** z. B. `-0.6152` (`25.9 %` KI-Wahrscheinlichkeit)
   * **2. Burstiness (Satzrhythmus):** z. B. $CV = 1.23$ (Hohe Varianz / Lebendiger Rhythmus)
   * **3. AI-Slop & Phrasen:** z. B. `9 Fundstellen (0.5 pro 1000 Wörter)`
   * **4. Formatierung:** z. B. `2.4 % Bulletpoints`
   * **Generierter Bericht:** Clickable Link `[dateiname_ki_analyse.md](file:///pfad/zur/datei_ki_analyse.md)`

2. **🔍 2. Erkannte Auffälligkeiten & Textstellen:**
   * Konkrete Signalwörter oder Phrasen mit Kontext nennen.

3. **💡 3. Handlungsempfehlung:**
   * Konkrete Hinweise zur Textoptimierung (z. B. Satzrhythmus beleben, Floskeln ersetzen).
