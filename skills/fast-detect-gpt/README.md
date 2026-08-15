# 🔬 Fast-DetectGPT Hybrid — AI Text Detector

> **Zero-Shot Erkennung von KI-generierten Texten** mit **3-Säulen-Hybridanalyse** (Fast-DetectGPT Wahrscheinlichkeitskrümmung auf GPU + Stilometrie/AI-Slop-Scanner + Burstiness & Strukturmetriken).

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PyTorch 2.12 cu128](https://img.shields.io/badge/PyTorch-CUDA%2012.8%20(sm__120)-EE4C2C.svg)](https://pytorch.org/)
[![ICLR 2024](https://img.shields.io/badge/ICLR-2024%20Paper-green.svg)](https://arxiv.org/abs/2310.05130)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 Überblick

Dieses Repository erweitert die Forschungsimplementierung von **Fast-DetectGPT** (*Bao et al., ICLR 2024*) zu einem praxistauglichen, industriellen Textprüf- und Gutachtensystem.

Anstatt Texte rein als mathematische „Blackbox“-Prozentzahl zu bewerten, kombiniert dieser Detektor die **lokale Wahrscheinlichkeitskrümmung auf der GPU** mit einer **regelbasierten Stilometrie- und Slop-Erkennung** sowie **statistischen Satzrhythmus-Metriken (Burstiness)**.

Ergebnisse werden bei jeder Prüfung automatisch als strukturierte **Markdown-Berichte (`.md`) mit Fundstellennachweis** und vollständiger Textarchivierung abgespeichert.

---

## 🧠 Das 3-Säulen-Bewertungsmodell im Detail

```
                  ┌────────────────────────────────────────────────────────┐
                  │              HYBRID KI-BEWERTUNG (100 %)               │
                  └──────────────────────────┬─────────────────────────────┘
                                             │
         ┌───────────────────────────────────┼──────────────────────────────────┐
         ▼ (60 % Gewichtung)                 ▼ (25 % Gewichtung)                ▼ (15 % Gewichtung)
┌──────────────────────────┐       ┌──────────────────────────┐       ┌──────────────────────────┐
│ 1. MATHEMATIK            │       │ 2. STILOMETRIE (SLOP)    │       │ 3. STRUKTUR & BURSTINESS │
├──────────────────────────┤       ├──────────────────────────┤       ├──────────────────────────┤
│ • Fast-DetectGPT         │       │ • Einleitungsfloskeln    │       │ • Satzrhythmus-Varianz   │
│ • Wahrscheinlichkeits-   │       │ • Stereotype Konnektoren │       │   ($CV = \sigma / \mu$)  │
│   krümmung (Curvature)   │       │ • KI-Lieblings-Buzzwords │       │ • Listen- & Bullet-Ratio │
│ • Lokale GPU-Inferenz    │       │ • Zeilengenaue Zitate    │       │ • Formatierungsdrang     │
└──────────────────────────┘       └──────────────────────────┘       └──────────────────────────┘
```

---

### Säule 1: Mathematische Wahrscheinlichkeitskrümmung (Fast-DetectGPT — 60 %)

Klassische Perplexitätsprüfer messen nur, wie wahrscheinlich einzelne Wörter für ein Sprachmodell sind. Menschliche Fachtexte (z. B. Jura oder Medizin) haben jedoch natürlicherweise eine geringe Perplexität, was oft zu Fehlalarmen führt.

**Fast-DetectGPT** löst dieses Problem über die **Krümmung der bedingten Wahrscheinlichkeitsdichte** (*Conditional Probability Curvature*). Es berechnet in einem einzigen Forward Pass auf der lokalen GPU die Diskrepanz zwischen der Log-Likelihood der Tokens und der erwarteten Bedingungswahrscheinlichkeit:

$$\text{Discrepancy} = \frac{\sum \log p(x_i) - \mu_{\text{ref}}}{\sqrt{\sum \sigma^2_{\text{ref}}}}$$

* **Kriterium $> +1.5$ ($\ge 75\,\%$)**: 🔴 **Stark KI-verdächtig** (Geringe Krümmungsvarianz, extrem glattgebügelte Tokenfolge).
* **Kriterium $0.0 \text{ bis } +1.5$ ($40\,\% - 75\,\%$)**: 🟡 **Gemischt / Überarbeitet** (Menschlicher Text mit KI-Politur oder formale Standardpassagen).
* **Kriterium $< 0.0$ ($< 40\,\%$)**: 🟢 **Menschlich verfasst** (Hohe natürliche Wortwahl-Varianz).

---

### Säule 2: Stilometrie & AI-Slop-Muster (25 %)

Sprachmodelle ohne starkes Prompting verfallen reproduzierbar in stereotype Floskeln, Füllwörter und Schein-Objektivität (*„AI-Slop“*). Der integrierte Stilometrie-Scanner prüft Texte auf Deutsch und Englisch auf:

1. **Typische Einleitungsfloskeln:**
   * *„In der heutigen, schnelllebigen / dynamischen Welt…“*
   * *„In einer Zeit, in der…“*
   * *„Es ist wichtig zu beachten / betonen, dass…“*
   * *„In today's fast-paced / rapidly changing world…“*
2. **Stereotype Konnektoren & Weichmacher:**
   * *„darüber hinaus“*, *„des Weiteren“*, *„nichtsdestotrotz“*, *„zusammenfassend lässt sich sagen“*, *„furthermore“*, *„moreover“*, *„it is worth noting that“*.
3. **KI-Lieblingsadjektive & Buzzwords:**
   * *„bahnbrechend“*, *„revolutionär“*, *„tiefgreifend“*, *„Meilenstein“*, *„Paradigmenwechsel“*, *„ganzheitlich“*, *„maßgeblich“*, *„groundbreaking“*, *„pivotal“*, *„seamless“*, *„testament to“*.
4. **Slop-Dichte (Treffer pro 1.000 Wörter):**
   * $\ge 6.0$: 🔴 Hohe Häufung
   * $2.0 - 6.0$: 🟡 Moderate Füllwortdichte
   * $< 2.0$: 🟢 Organische Sprache

---

### Säule 3: Struktur & Satzrhythmus / Burstiness (15 %)

Menschliche Sprache atmet durch **Burstiness** — einen ständigen Wechsel zwischen ultrakurzen Thesensätzen, rhythmischen Einschüben und verschachtelten Satzgefügen. LLMs generieren hingegen monotone Sätze in einem gleichförmigen Takt.

1. **Variationskoeffizient der Satzlängen ($CV = \frac{\sigma}{\mu}$):**
   * **$CV \ge 0.55$**: 🟢 **Hohe Varianz (Menschlich)** — Natürliche, lebendige Rhythmuswechsel.
   * **$CV < 0.35$**: 🔴 **Geringe Varianz (KI-Monotonie)** — Starre Taktung um 14–22 Wörter pro Satz.
2. **Listen-Dichte (Bulletpoint-Ratio):**
   * Misst den Anteil von Aufzählungszeilen am Gesamttext. Ein übermäßiger Listenanteil ($\ge 35\,\%$) signalisiert den typischen KI-Formatierungsdrang.

---

### 🎯 Gesamteinstufung (Hybrid-Synthese)

Alle drei Säulen fließen gewichtet in den finalen **Hybrid-Score** ein:

$$\text{Score}_{\text{Hybrid}} = 0.60 \cdot \text{Score}_{\text{FastDetect}} + 0.25 \cdot \text{Score}_{\text{Slop}} + 0.15 \cdot \text{Score}_{\text{Structure}}$$

| Gesamtscore | Einstufung | Bedeutung |
|:---:|---|---|
| **$\ge 75\,\%$** | 🔴 **Sehr wahrscheinlich KI-generiert** | Monotoner Takt, hohe Slop-Dichte, mathematisch minimale Krümmung. |
| **$40\,\% - 75\,\%$** | 🟡 **Gemischt / Teilweise KI-unterstützt** | Menschlicher Kern mit KI-Politur, formalisierte Tabellen/Listen oder Standardgliederungen. |
| **$< 40\,\%$** | 🟢 **Sehr wahrscheinlich menschlich** | Hohe Burstiness ($CV \ge 0.55$), unvorhersehbare Wortkombinationen, organische Gedankenführung. |

---

## 🚀 Schnellstart & Nutzung

### Voraussetzungen & GPU-Support
* **Python:** `>=3.11, <3.12`
* **Paketmanager:** [`uv`](https://github.com/astral-sh/uv) (empfohlen)
* **GPU-Unterstützung:** PyTorch mit **CUDA 12.8** (Unterstützt alle NVIDIA RTX GPUs inkl. RTX 50-Serie / Blackwell `sm_120`).

### 1. Ganze Datei prüfen (.pdf, .txt, .md)
```bash
uv run python detect_text.py --file "D:\Dokumente\Mein_Aufsatz.pdf" --device cuda
```
> 📁 **Automatischer Speicherort:** Der Bericht wird als `Mein_Aufsatz_ki_analyse.md` **direkt im selben Verzeichnis wie die PDF-Datei** abgelegt.

### 2. Direkttext / Copy & Paste prüfen
```bash
uv run python detect_text.py --text "In der heutigen dynamischen Welt ist es von entscheidender Bedeutung..." --device cuda
```
> 📁 **Automatischer Speicherort:** Der Bericht wird in den Ordner `./dokumente/ki_analyse_YYYYMMDD_HHMMSS_<snippet>.md` geschrieben und **enthält den vollständigen Originaltext** zur Nachvollziehbarkeit.

### 3. Interaktiver Modus (PowerShell-Starter)
```powershell
.\detect.ps1
```

---

## 📄 Beispiel eines generierten Analyseberichts

Jeder erzeugte Markdown-Bericht enthält eine strukturierte Übersicht:

```markdown
# 🔬 KI-Texterkennungsbericht (Hybrid-Analyse)

| Dimension | Ergebnis / Metrik | Einstufung |
|---|---|---|
| **🎯 Gesamtergebnis (Hybrid)** | **17.9 % KI-Wahrscheinlichkeit** | **🟢 SEHR WAHRSCHEINLICH MENSCHLICH VERFASST** |
| **1. Fast-DetectGPT (Mathematik)** | Curvature: `-0.6152` | 25.9 % KI-Wahrscheinlichkeit |
| **2. Burstiness (Satzrhythmus)** | $CV = 1.23$ ($\mu = 14.2$, $\sigma = 17.5$) | 🟢 Hohe Varianz (Lebendiger Rhythmus) |
| **3. AI-Slop & Signalwörter** | 9 Treffer (0.5 pro 1000 Wörter) | 🟢 Kaum auffällige KI-Floskeln |
| **4. Struktur & Listen-Dichte** | 2.4 % Bulletpoint-Zeilen | 🟢 Natürlich strukturierter Fließtext |

### Erkannte Signalwörter & AI-Slop-Muster:
| Zeile | Kategorie | Gefundene Phrase | Kontext-Ausschnitt |
|---|---|---|---|
| Z. 14 | Stereotyper Konnektor | **`darüber hinaus`** | *„...darüber hinaus bleibt festzuhalten...“* |
```

---

## 📚 Wissenschaftliche Referenz

Falls du Fast-DetectGPT zitieren möchtest:

```bibtex
@inproceedings{bao2023fast,
  title={Fast-DetectGPT: Efficient Zero-Shot Detection of Machine-Generated Text via Conditional Probability Curvature},
  author={Bao, Guangsheng and Zhao, Yanbin and Teng, Zhiyang and Yang, Linyi and Zhang, Yue},
  booktitle={The Twelfth International Conference on Learning Representations (ICLR)},
  year={2024}
}
```
