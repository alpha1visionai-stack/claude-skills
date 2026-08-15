---
name: fast-detect-gpt
description: Zero-Shot Erkennung von KI-generierten Texten (ChatGPT, GPT-4, LLaMA, Claude, Mistral) mit Fast-DetectGPT (Bao et al., ICLR 2024). Analysiert Text oder Dateien auf KI-Echtheit, berechnet die exakte KI-Wahrscheinlichkeit und deckt KI-Slop auf. Speichert automatisch vollständige Markdown-Berichte (.md) im Dateiverzeichnis bzw. im Ordner dokumente/. Verwenden, wenn der Benutzer sagt oder andeutet: "bitte prüfe den text auf KI generierung", "prüfe auf KI", "ist dieser Text von einer KI geschrieben?", "KI-Check", "KI Text Detektor", "prüfe Datei auf KI", "KI Erkennung" oder ähnliche Aufforderungen zur KI-Texterkennung.
---

# Fast-DetectGPT — AI Text Detector Skill

Dieser Skill analysiert übergebene Texte oder Dateien (PDF, Markdown, Textdateien, Aufsätze, Hausarbeiten, Blogbeiträge, Quelltexte), um objektiv und mathematisch fundiert festzustellen, ob sie von einer künstlichen Intelligenz (ChatGPT, GPT-4, Claude, Mistral, LLaMA) oder von einem Menschen verfasst wurden.

---

## ⚙️ Funktionsweise im Hintergrund

Fast-DetectGPT (*Bao et al., ICLR 2024*) berechnet die **Krümmung der bedingten Wahrscheinlichkeit** (*Conditional Probability Curvature*) über eine geschlossene analytische Formel in einem einzigen Modell-Durchlauf (Single Forward Pass auf der lokalen NVIDIA RTX GPU):

$$\text{Discrepancy} = \frac{\sum \log p(x_i) - \mu_{\text{ref}}}{\sqrt{\sum \sigma^2_{\text{ref}}}}$$

* **Kriterium > +1.5 ($\ge$ 75 %)**: 🔴 **Sehr wahrscheinlich KI-generiert** (geringe Varianz, extrem vorhersehbare Token).
* **Kriterium 0.0 bis +1.5 (40 % – 75 %)**: 🟡 **Gemischt / Überarbeitet** (Menschlicher Text mit KI-Politur oder stark formalisierte Fachsprache).
* **Kriterium < 0.0 (< 40 %)**: 🟢 **Sehr wahrscheinlich menschlich** (hohe natürliche Wort- und Satzrhythmus-Varianz / Burstiness).

---

## 🛠️ Ausführungspfade & Befehle

Die lokale Fast-DetectGPT-Installation befindet sich unter:
`D:\OneDrive\Development\fast-detect-gpt`

### 1. Bei direkt im Chat eingefügtem Text (Copy & Paste):
Führe das Python-Tool direkt über `uv run` aus (Nutzt GPU `cuda`):

```bash
uv run --directory "D:\OneDrive\Development\fast-detect-gpt" python detect_text.py --text "<Hier steht der zu prüfende Text>" --device cuda
```
> **Automatischer Speicherort:** Wird automatisch als `.md`-Bericht in das Verzeichnis `./dokumente/` des Projektordners geschrieben (z. B. `dokumente/ki_analyse_20260815_115031_beispiel.md`) und **enthält den vollständigen analysierten Originaltext**.

### 2. Bei Dateien (.pdf, .txt, .md):
Übergib den Dateipfad mit dem `--file` Parameter:

```bash
uv run --directory "D:\OneDrive\Development\fast-detect-gpt" python detect_text.py --file "<Dateipfad>" --device cuda
```
> **Automatischer Speicherort:** Wird automatisch als `.md`-Bericht im **selben Verzeichnis wie die Quelldatei** abgelegt (z. B. `<verzeichnis>/<dateiname>_ki_analyse.md`).

---

## 📋 Antwortformat für den Benutzer

Fasse das Ergebnis nach der Ausführung für den Benutzer in folgender klarer Struktur zusammen und verlinke immer den erzeugten Bericht:

1. **📊 1. Analyse-Ergebnis:**
   * **Fast-DetectGPT Kriterium (Curvature):** z. B. `-0.6152`
   * **Mittlere KI-Wahrscheinlichkeit:** z. B. `25.9 %`
   * **Einstufung:** 🟢 Menschlich / 🟡 Gemischt / 🔴 KI-generiert
   * **Analysierter Umfang:** z. B. `60 Abschnitte (17.186 Wörter / 50.717 Tokens)`
   * **Generierter Bericht:** Clickable Link `[dateiname_ki_analyse.md](file:///pfad/zur/datei_ki_analyse.md)`

2. **🔍 2. Stilistische Analyse & Auffälligkeiten:**
   * Welche konkreten sprachlichen Merkmale (KI-Floskeln, stereotype Konnektoren, monotone Syntax vs. organische Gedankenführung) stützen den berechneten Score?

3. **💡 3. Handlungsempfehlung:**
   * Konkrete Optimierungsvorschläge bei Bedarf.
