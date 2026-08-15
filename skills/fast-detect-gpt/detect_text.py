#!/usr/bin/env python3
"""
Fast-DetectGPT Convenience CLI & Python Tool
Evaluates German and English texts to detect AI-generated content using conditional probability curvature.
Automatically generates and saves comprehensive markdown reports (.md).
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime
import re

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Add scripts directory to sys.path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

import torch
import numpy as np
from local_infer import FastDetectGPT

def chunk_text(text: str, target_words: int = 400):
    """Splits long texts into readable thematic paragraph chunks."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        paragraphs = [text.strip()]
        
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for p in paragraphs:
        w_count = len(p.split())
        if current_word_count + w_count > target_words and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [p]
            current_word_count = w_count
        else:
            current_chunk.append(p)
            current_word_count += w_count
            
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
        
    return chunks

def extract_content_from_file(file_path: Path) -> str:
    """Extracts text content from various file formats (.txt, .md, .pdf)."""
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(file_path))
            pages_text = [page.extract_text() or "" for page in reader.pages]
            return "\n\n".join(pages_text).strip()
        except Exception as e:
            print(f"[!] Fehler beim Extrahieren aus PDF: {e}")
            raise
    else:
        # Default text/markdown reading
        try:
            return file_path.read_text(encoding="utf-8").strip()
        except UnicodeDecodeError:
            return file_path.read_text(encoding="latin-1", errors="replace").strip()

def evaluate_and_report(detector, text: str, source_type: str = "text", file_path: Path = None, output_dir: Path = None):
    text = text.strip()
    if not text:
        print("[!] Leerer Text übergeben.")
        return None

    words_total = len(text.split())
    chunks = chunk_text(text, target_words=400)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now_file_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    section_results = []
    for idx, ch in enumerate(chunks):
        first_line = ch.split("\n")[0][:80].strip()
        prob, crit, ntokens = detector.compute_prob(ch)
        prob_pct = prob * 100.0

        if prob_pct >= 75.0:
            status = "🔴 KI-GENERIERT"
        elif prob_pct >= 40.0:
            status = "🟡 GEMISCHT / ÜBERARBEITET"
        else:
            status = "🟢 MENSCHLICH"

        section_results.append({
            "id": idx + 1,
            "title": first_line,
            "criterion": float(crit),
            "prob_pct": float(prob_pct),
            "tokens": int(ntokens),
            "words": len(ch.split()),
            "status": status,
            "snippet": ch[:250]
        })

    # Global aggregation
    criteria = [r["criterion"] for r in section_results]
    probs = [r["prob_pct"] for r in section_results]
    total_tokens = sum(r["tokens"] for r in section_results)

    mean_crit = float(np.mean(criteria))
    median_crit = float(np.median(criteria))
    mean_prob = float(np.mean(probs))
    median_prob = float(np.median(probs))

    ai_count = sum(1 for r in section_results if r["prob_pct"] >= 75.0)
    mixed_count = sum(1 for r in section_results if 40.0 <= r["prob_pct"] < 75.0)
    human_count = sum(1 for r in section_results if r["prob_pct"] < 40.0)

    if mean_prob >= 75.0:
        overall_verdict = "🔴 SEHR WAHRSCHEINLICH KI-GENERIERT"
    elif mean_prob >= 40.0:
        overall_verdict = "🟡 GEMISCHT / TEILWEISE KI-UNTERSTÜTZT"
    else:
        overall_verdict = "🟢 SEHR WAHRSCHEINLICH MENSCHLICH VERFASST"

    # Terminal Output
    print("\n" + "=" * 70)
    if file_path:
        print(f"📄 Analyse-Datei: {file_path.name}")
    else:
        print(f"📝 Analyse: Direkt übergebener Text")
    print("-" * 70)
    print(f"• Fast-DetectGPT Kriterium (Curvature): {mean_crit:+.4f} (Median: {median_crit:+.4f})")
    print(f"• Mittlere KI-Wahrscheinlichkeit:        {mean_prob:.1f}% (Median: {median_prob:.1f}%)")
    print(f"• Ergebnis-Einstufung:                  {overall_verdict}")
    print(f"• Analysierter Gesamtumfang:            {len(section_results)} Abschnitte ({words_total} Wörter / {total_tokens} Tokens)")
    print(f"• Verteilung:                           🟢 {human_count} Menschlich | 🟡 {mixed_count} Gemischt | 🔴 {ai_count} KI")
    print("=" * 70)

    # Determine Destination Markdown File
    if source_type == "file" and file_path:
        target_dir = file_path.parent
        # Clean stem
        stem = file_path.stem
        if stem.lower().endswith(".md"):
            stem = stem[:-3]
        clean_stem = re.sub(r'[\s]+', '_', stem)
        report_file = target_dir / f"{clean_stem}_ki_analyse.md"
    else:
        # Copy & Paste Text Mode -> Save in 'dokumente' folder of working directory
        if output_dir:
            target_dir = Path(output_dir)
        else:
            target_dir = Path.cwd() / "dokumente"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Snippet for file name
        snippet_words = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß]+', '_', text[:30]).strip('_')
        if not snippet_words:
            snippet_words = "text"
        report_file = target_dir / f"ki_analyse_{now_file_str}_{snippet_words[:20]}.md"

    # Build Markdown Content
    md_lines = [
        f"# 🔬 KI-Texterkennungsbericht — Fast-DetectGPT",
        f"",
        f"**Datum & Uhrzeit:** {now_str}  ",
        f"**Analyse-Methode:** Fast-DetectGPT (*Bao et al., ICLR 2024* — Conditional Probability Curvature)  ",
        f"**Modell & Hardware:** `{detector.args.sampling_model_name}` / `{detector.args.scoring_model_name}` auf `{detector.args.device.upper()}`  ",
    ]

    if file_path:
        md_lines.append(f"**Quelldatei:** `{file_path.name}` ([Dateipfad](file:///{str(file_path).replace(chr(92), '/')}))  ")
    else:
        md_lines.append(f"**Quelle:** Direkt eingefügter Text (Copy & Paste)  ")

    md_lines.extend([
        f"",
        f"---",
        f"",
        f"## 📊 1. Zusammenfassung & Kernmetriken",
        f"",
        f"| Metrik | Wert |",
        f"|---|---|",
        f"| **Gesamteinstufung** | **{overall_verdict}** |",
        f"| **Mittlere KI-Wahrscheinlichkeit** | **{mean_prob:.1f} %** (Median: {median_prob:.1f} %) |",
        f"| **Curvature-Kriterium (Discrepancy)** | **{mean_crit:+.4f}** (Median: {median_crit:+.4f}) |",
        f"| **Analysierter Umfang** | {len(section_results)} Abschnitte ({words_total} Wörter / {total_tokens} Tokens) |",
        f"| **🟢 Menschliche Abschnitte (< 40 %)** | {human_count} ({human_count / len(section_results) * 100:.1f} %) |",
        f"| **🟡 Gemischte Abschnitte (40–75 %)** | {mixed_count} ({mixed_count / len(section_results) * 100:.1f} %) |",
        f"| **🔴 KI-generierte Abschnitte (≥ 75 %)** | {ai_count} ({ai_count / len(section_results) * 100:.1f} %) |",
        f"",
        f"---",
        f"",
        f"## 📈 2. Abschnittsweise Detailauswertung",
        f"",
        f"| # | Abschnitt / Titel | Wörter | Tokens | Kriterium | KI-Score | Einstufung |",
        f"|---|---|---|---|---|---|---|",
    ])

    for r in section_results:
        clean_title = r["title"].replace("|", "\\|")
        md_lines.append(
            f"| {r['id']:02d} | `{clean_title}` | {r['words']} | {r['tokens']} | `{r['criterion']:+.4f}` | **{r['prob_pct']:.1f} %** | {r['status']} |"
        )

    # Stylistic Insights & Recommendations
    md_lines.extend([
        f"",
        f"---",
        f"",
        f"## 🔍 3. Stilistische Interpretation & Befund",
        f"",
        f"* **Krümmungs-Interpretation:** Fast-DetectGPT analysiert die lokale Krümmung der Wahrscheinlichkeitsdichte um die Token-Sequenzen. Menschliche Texte weisen typischerweise negative Kriterien auf (hohe Wortwahl-Varianz und unvorhersehbare Rhythmus-Wechsel / *Burstiness*). Maschinell generierte Texte clustern sich bei positiven Kriterien (> +1.5 / ≥ 75 %).",
        f"* **Auffälligkeiten:** Abschnitte mit erhöhten Werten zeichnen sich meist durch stark formelhafte Satzanschlüsse, monotone syntaktische Strukturen oder stereotype Aufzählungen aus.",
        f"",
    ])

    # If Copy & Paste text, include the original text
    if source_type == "text" or not file_path:
        md_lines.extend([
            f"---",
            f"",
            f"## 📝 4. Analysierter Originaltext",
            f"",
            f"```text",
            text,
            f"```",
            f""
        ])

    # Write report file
    report_file.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"\n[✓] Analysebericht erfolgreich gespeichert: {report_file.resolve()}")

    return {
        "report_file": str(report_file.resolve()),
        "mean_criterion": mean_crit,
        "mean_probability": mean_prob,
        "overall_verdict": overall_verdict,
        "total_words": words_total,
        "total_tokens": total_tokens,
        "sections": section_results
    }

def main():
    parser = argparse.ArgumentParser(
        description="Fast-DetectGPT: Schnelle Zero-Shot Erkennung von KI-generiertem Text mit automatischer Markdown-Berichterstellung"
    )
    parser.add_argument(
        "--text", "-t", type=str, help="Der zu analysierende Text (in Anführungszeichen)"
    )
    parser.add_argument(
        "--file", "-f", type=str, help="Pfad zu einer Text-, Markdown- oder PDF-Datei"
    )
    parser.add_argument(
        "--output_dir", "-o", type=str, default=None, help="Optionales Ausgabeverzeichnis für Textberichte (Standard: ./dokumente)"
    )
    parser.add_argument(
        "--sampling_model_name",
        type=str,
        default="gpt-neo-2.7B",
        choices=["gpt-neo-2.7B", "gpt-j-6B", "falcon-7b"],
        help="Sampling-Modell (Standard: gpt-neo-2.7B)"
    )
    parser.add_argument(
        "--scoring_model_name",
        type=str,
        default="gpt-neo-2.7B",
        choices=["gpt-neo-2.7B", "gpt-j-6B", "falcon-7b-instruct"],
        help="Scoring-Modell (Standard: gpt-neo-2.7B)"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="Ausführungsgerät (cuda oder cpu)"
    )
    parser.add_argument(
        "--cache_dir",
        type=str,
        default=os.path.expanduser("~/.cache/huggingface/hub"),
        help="Hugging Face Cache-Verzeichnis"
    )

    args = parser.parse_args()

    print(f">> Initialisiere Fast-DetectGPT auf {args.device.upper()}...")
    print(f"• Sampling Model: {args.sampling_model_name}")
    print(f"• Scoring Model:  {args.scoring_model_name}")

    detector = FastDetectGPT(args)
    print(">> Modell erfolgreich geladen!\n")

    if args.text:
        evaluate_and_report(detector, args.text, source_type="text", output_dir=args.output_dir)
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"[-] Datei nicht gefunden: {file_path}")
            sys.exit(1)
        content = extract_content_from_file(file_path)
        evaluate_and_report(detector, content, source_type="file", file_path=file_path)
    else:
        # Interactive mode
        print(">> Interaktiver Modus: Fuege deinen Text ein.")
        print("Druecke [ENTER] und danach nochmals [ENTER] (Leerzeile), um die Analyse zu starten.")
        print("Tippe 'exit' oder druecke Strg+C zum Beenden.\n")

        while True:
            try:
                print("Text eingeben:")
                lines = []
                while True:
                    line = input()
                    if line.strip().lower() == "exit":
                        print("Auf Wiedersehen!")
                        return
                    if len(line) == 0:
                        break
                    lines.append(line)
                raw_text = "\n".join(lines).strip()
                if not raw_text:
                    continue
                evaluate_and_report(detector, raw_text, source_type="text", output_dir=args.output_dir)
            except KeyboardInterrupt:
                print("\nProgramm beendet.")
                break

if __name__ == "__main__":
    main()
