#!/usr/bin/env python3
"""
Fast-DetectGPT Hybrid AI Text Detector
Combines:
1. Fast-DetectGPT (Bao et al., ICLR 2024) — Conditional Probability Curvature on GPU
2. Stylometric AI-Slop & Phrasen-Analyse (Heuristische Signalwörter & Füllphrasen)
3. Strukturanalyse & Burstiness (Satzlängen-Varianz & Listen-Dichte)
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
from stylometry import (
    analyze_burstiness,
    analyze_slop_and_phrases,
    analyze_structure,
    compute_hybrid_assessment
)

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
        try:
            return file_path.read_text(encoding="utf-8").strip()
        except UnicodeDecodeError:
            return file_path.read_text(encoding="latin-1", errors="replace").strip()

def evaluate_and_report(detector, text: str, source_type: str = "text", file_path: Path = None, output_dir: Path = None):
    text = text.strip()
    if not text:
        print("[!] Leerer Text übergeben.")
        return None

    words_total = len(re.findall(r'\b\w+\b', text))
    chunks = chunk_text(text, target_words=400)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now_file_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 1. Fast-DetectGPT (Mathematical Curvature)
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

    criteria = [r["criterion"] for r in section_results]
    probs = [r["prob_pct"] for r in section_results]
    total_tokens = sum(r["tokens"] for r in section_results)

    mean_crit = float(np.mean(criteria))
    median_crit = float(np.median(criteria))
    mean_fast_prob = float(np.mean(probs))
    median_fast_prob = float(np.median(probs))

    ai_count = sum(1 for r in section_results if r["prob_pct"] >= 75.0)
    mixed_count = sum(1 for r in section_results if 40.0 <= r["prob_pct"] < 75.0)
    human_count = sum(1 for r in section_results if r["prob_pct"] < 40.0)

    # 2. Stylometric & Burstiness & Structural Analysis
    burstiness_res = analyze_burstiness(text)
    slop_res = analyze_slop_and_phrases(text)
    struct_res = analyze_structure(text)

    # 3. Hybrid Assessment
    hybrid_res = compute_hybrid_assessment(
        fast_detect_prob=(mean_fast_prob / 100.0),
        burstiness_res=burstiness_res,
        slop_res=slop_res,
        structure_res=struct_res
    )
    overall_verdict = hybrid_res["overall_verdict"]
    hybrid_pct = hybrid_res["hybrid_probability_pct"]

    # Terminal Output
    print("\n" + "=" * 75)
    if file_path:
        print(f"📄 Analyse-Datei: {file_path.name}")
    else:
        print(f"📝 Analyse: Direkt übergebener Text")
    print("-" * 75)
    print(f"• 🎯 Hybrid-Gesamtergebnis:             {overall_verdict} ({hybrid_pct:.1f}%)")
    print(f"• 1. Fast-DetectGPT (Curvature):       {mean_crit:+.4f} | Prob: {mean_fast_prob:.1f}%")
    print(f"• 2. Burstiness / Satzrhythmus:        CV={burstiness_res['cv']:.2f} | {burstiness_res['verdict']}")
    print(f"• 3. AI-Slop & Phrasendichte:          {slop_res['total_hits']} Fundstellen ({slop_res['density_per_1000_words']:.1f}/1000 Wörter)")
    print(f"• 4. Formatierung / Listen-Dichte:     {struct_res['bullet_ratio_pct']:.1f}% Bulletpoints | {struct_res['verdict']}")
    print(f"• Analysierter Umfang:                 {len(section_results)} Abschnitte ({words_total} Wörter / {total_tokens} Tokens)")
    print("=" * 75)

    # Determine Destination Markdown File
    if source_type == "file" and file_path:
        target_dir = file_path.parent
        stem = file_path.stem
        if stem.lower().endswith(".md"):
            stem = stem[:-3]
        clean_stem = re.sub(r'[\s]+', '_', stem)
        report_file = target_dir / f"{clean_stem}_ki_analyse.md"
    else:
        if output_dir:
            target_dir = Path(output_dir)
        else:
            target_dir = Path.cwd() / "dokumente"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        snippet_words = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß]+', '_', text[:30]).strip('_')
        if not snippet_words:
            snippet_words = "text"
        report_file = target_dir / f"ki_analyse_{now_file_str}_{snippet_words[:20]}.md"

    # Build Markdown Content
    md_lines = [
        f"# 🔬 KI-Texterkennungsbericht (Hybrid-Analyse)",
        f"",
        f"**Datum & Uhrzeit:** {now_str}  ",
        f"**Methodik:** 3-Säulen-Hybridanalyse (Fast-DetectGPT Wahrscheinlichkeitskrümmung + Stilometrie/Slop + Struktur/Burstiness)  ",
        f"**Hardware & Modell:** `{detector.args.sampling_model_name}` / `{detector.args.scoring_model_name}` auf `{detector.args.device.upper()}`  ",
    ]

    if file_path:
        md_lines.append(f"**Quelldatei:** `{file_path.name}` ([Dateipfad](file:///{str(file_path).replace(chr(92), '/')}))  ")
    else:
        md_lines.append(f"**Quelle:** Direkt eingefügter Text (Copy & Paste)  ")

    md_lines.extend([
        f"",
        f"---",
        f"",
        f"## 📊 1. Zusammenfassung & Hybrid-Gesamtergebnis",
        f"",
        f"| Dimension | Ergebnis / Metrik | Einstufung |",
        f"|---|---|---|",
        f"| **🎯 Gesamtergebnis (Hybrid)** | **{hybrid_pct:.1f} % KI-Wahrscheinlichkeit** | **{overall_verdict}** |",
        f"| **1. Fast-DetectGPT (Mathematik)** | Curvature: `{mean_crit:+.4f}` (Median: `{median_crit:+.4f}`) | {mean_fast_prob:.1f} % KI-Wahrscheinlichkeit |",
        f"| **2. Burstiness (Satzrhythmus)** | $CV = {burstiness_res['cv']:.2f}$ ($\mu = {burstiness_res['mean_length']:.1f}$, $\sigma = {burstiness_res['std_length']:.1f}$) | {burstiness_res['verdict']} |",
        f"| **3. AI-Slop & Signalwörter** | {slop_res['total_hits']} Treffer ({slop_res['density_per_1000_words']:.1f} pro 1000 Wörter) | {slop_res['verdict']} |",
        f"| **4. Struktur & Listen-Dichte** | {struct_res['bullet_ratio_pct']:.1f} % Bulletpoint-Zeilen | {struct_res['verdict']} |",
        f"| **Analysierter Umfang** | {len(section_results)} Abschnitte, {burstiness_res['sentence_count']} Sätze ({words_total} Wörter / {total_tokens} Tokens) | - |",
        f"",
        f"---",
        f"",
        f"## 📈 2. Abschnittsweise Fast-DetectGPT Detailauswertung",
        f"",
        f"| # | Abschnitt / Titel | Wörter | Tokens | Kriterium | KI-Score | Einstufung |",
        f"|---|---|---|---|---|---|---|",
    ])

    for r in section_results:
        clean_title = r["title"].replace("|", "\\|")
        md_lines.append(
            f"| {r['id']:02d} | `{clean_title}` | {r['words']} | {r['tokens']} | `{r['criterion']:+.4f}` | **{r['prob_pct']:.1f} %** | {r['status']} |"
        )

    # Slop Findings Table
    md_lines.extend([
        f"",
        f"---",
        f"",
        f"## 🔍 3. Erkannte Signalwörter & AI-Slop-Muster ({slop_res['total_hits']} Fundstellen)",
        f"",
    ])

    if slop_res["findings"]:
        md_lines.extend([
            f"| Zeile | Kategorie | Gefundene Phrase | Kontext-Ausschnitt |",
            f"|---|---|---|---|",
        ])
        for hit in slop_res["findings"][:30]:  # Cap table at top 30
            clean_ctx = hit["context"].replace("|", "\\|").replace("\n", " ")
            md_lines.append(f"| Z. {hit['line']} | {hit['category']} | **`{hit['phrase']}`** | *„...{clean_ctx}...“* |")
        if len(slop_res["findings"]) > 30:
            md_lines.append(f"\n*... und {len(slop_res['findings']) - 30} weitere Fundstellen.*")
    else:
        md_lines.append(f"*(Keine typischen AI-Slop-Phrasen oder repetitiven Füllwörter gefunden.)*")

    # Burstiness & Structure Detail
    md_lines.extend([
        f"",
        f"---",
        f"",
        f"## 📐 4. Statistische Rhythmus- & Strukturdaten",
        f"",
        f"* **Satzlängen-Verteilung:** Min: `{burstiness_res['min_length']}` Wörter, Max: `{burstiness_res['max_length']}` Wörter, Mittelwert ($\mu$): `{burstiness_res['mean_length']:.1f}` Wörter, Median: `{burstiness_res['median_length']:.1f}` Wörter.",
        f"* **Variationskoeffizient ($CV = \sigma / \mu$):** `{burstiness_res['cv']:.2f}` (Werte $\ge 0.55$ deuten auf organischen, abwechslungsreichen Menschenrhythmus hin; Werte $< 0.35$ auf maschinelle Monotonie).",
        f"* **Layout & Formatierung:** `{struct_res['bullet_count']}` von `{struct_res['total_lines']}` Zeilen sind Aufzählungspunkte ({struct_res['bullet_ratio_pct']:.1f} %).",
        f"",
    ])

    # If Copy & Paste text, include the original text
    if source_type == "text" or not file_path:
        md_lines.extend([
            f"---",
            f"",
            f"## 📝 5. Analysierter Originaltext",
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
        "hybrid_score": hybrid_res,
        "fast_detect": {
            "mean_criterion": mean_crit,
            "mean_probability": mean_fast_prob,
            "sections": section_results
        },
        "burstiness": burstiness_res,
        "slop": slop_res,
        "structure": struct_res
    }

def main():
    parser = argparse.ArgumentParser(
        description="Fast-DetectGPT Hybrid: Zero-Shot KI-Texterkennung mit Wahrscheinlichkeitskrümmung, Stilometrie und Burstiness-Analyse"
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

    print(f">> Initialisiere Fast-DetectGPT Hybrid auf {args.device.upper()}...")
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
