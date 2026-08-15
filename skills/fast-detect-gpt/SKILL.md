---
name: fast-detect-gpt
description: Zero-Shot Erkennung von KI-generierten Texten (ChatGPT, GPT-4, LLaMA, Claude, Mistral) mit Fast-DetectGPT (Bao et al., ICLR 2024). Analysiert Text oder Dateien auf KI-Echtheit, berechnet die exakte KI-Wahrscheinlichkeit und deckt KI-Slop auf. Verwenden, wenn der Benutzer sagt oder andeutet: "bitte prüfe den text auf KI generierung", "prüfe auf KI", "ist dieser Text von einer KI geschrieben?", "KI-Check", "KI Text Detektor", "prüfe Datei auf KI", "KI Erkennung" oder ähnliche Aufforderungen zur KI-Texterkennung.
---

# Fast-DetectGPT — AI Text Detector Skill

Dieser Skill analysiert übergebene Texte oder Dateien (Aufsätze, Hausarbeiten, Blogbeiträge, Quelltexte), um objektiv und mathematisch fundiert festzustellen, ob sie von einer künstlichen Intelligenz (ChatGPT, GPT-4, Claude, Mistral, LLaMA) oder von einem Menschen verfasst wurden.

---

## ⚙️ Funktionsweise im Hintergrund

Fast-DetectGPT (*Bao et al., ICLR 2024*) berechnet die **Krümmung der bedingten Wahrscheinlichkeit** (*Conditional Probability Curvature*) über eine geschlossene analytische Formel in einem einzigen Modell-Durchlauf (Single Forward Pass auf der lokalen NVIDIA GPU):

$$\text{Discrepancy} = \frac{\sum \log p(x_i) - \mu_{\text{ref}}}{\sqrt{\sum \sigma^2_{\text{ref}}}}$$

* **Kriterium > +1.5 ($\ge$ 75 %)**: 🔴 **Sehr wahrscheinlich KI-generiert** (geringe Varianz, extrem vorhersehbare Token).
* **Kriterium 0.0 bis +1.5 (40 % – 75 %)**: 🟡 **Gemischt / Überarbeitet** (Menschlicher Text mit KI-Politur oder stark formalisierte Fachsprache).
* **Kriterium < 0.0 (< 40 %)**: 🟢 **Sehr wahrscheinlich menschlich** (hohe natürliche Wort- und Satzrhythmus-Varianz / Burstiness).

---

## 🛠️ Ausführungspfade & Befehle

Die lokale Fast-DetectGPT-Installation befindet sich unter:
`D:\OneDrive\Development\fast-detect-gpt`

### 1. Bei direkt im Chat eingefügtem Text:
Führe das Python-Tool direkt über `uv run` aus:

```bash
uv run --directory "D:\OneDrive\Development\fast-detect-gpt" python detect_text.py --text "<Hier steht der zu prüfende Text>"
```

### 2. Bei längeren Texten, Absätzen oder Dateipfaden (.txt, .md):
Wenn der Benutzer einen Dateipfad angibt oder der Text sehr lang/mehrzeilig ist, speichere den Text bei Bedarf kurz in einer Datei und führe aus:

```bash
uv run --directory "D:\OneDrive\Development\fast-detect-gpt" python detect_text.py --file "<Dateipfad>"
```

---

## 📋 Antwortformat für den Benutzer

Fasse das Ergebnis nach der Ausführung für den Benutzer immer in folgender klarer Struktur zusammen:

1. **📊 Analyse-Ergebnis:**
   * **Fast-DetectGPT Kriterium:** z. B. `+3.2505`
   * **KI-Wahrscheinlichkeit:** z. B. `92.4 %`
   * **Einstufung:** 🔴 KI-generiert / 🟡 Gemischt / 🟢 Menschlich
   * **Analysierte Token:** z. B. `73 Tokens`

2. **🔍 Stilistische Analyse:**
   * Welche konkreten sprachlichen Merkmale (KI-Floskeln wie *„In der heutigen dynamischen Welt...“*, stereotype Konnektoren, monotone Satzstrukturen vs. organische menschliche Gedankenführung) stützen den berechneten Score?

3. **💡 Handlungsempfehlung:**
   * Wie kann der Text bei Bedarf natürlicher und lebendiger gestaltet werden (z. B. durch Variation der Satzlängen und Beseitigung von KI-Phrasen)?
