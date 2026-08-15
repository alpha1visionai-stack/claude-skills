#!/usr/bin/env python3
"""
Fast-DetectGPT Convenience CLI & Python Tool
Evaluates German and English texts to detect AI-generated content using conditional probability curvature.
"""

import sys
import os
import argparse
from pathlib import Path

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

def evaluate_text(detector, text: str, title: str = ""):
    text = text.strip()
    if not text:
        print("[!] Leerer Text übergeben.")
        return None

    prob, crit, ntokens = detector.compute_prob(text)
    prob_pct = prob * 100.0

    # Determine verdict category
    if prob_pct >= 75.0:
        verdict = "[KI] SEHR WAHRSCHEINLICH KI-GENERIERT"
    elif prob_pct >= 40.0:
        verdict = "[?] GEMISCHT / TEILWEISE KI-UNTERSTUETZT (UNSICHER)"
    else:
        verdict = "[HUMAN] SEHR WAHRSCHEINLICH MENSCHLICH VERFASST"

    print("\n" + "=" * 65)
    if title:
        print(f"Analyse: {title}")
        print("-" * 65)
    print(f"Fast-DetectGPT Kriterium (Curvature): {crit:.4f}")
    print(f"KI-Wahrscheinlichkeit:                {prob_pct:.1f}%")
    print(f"Ergebnis-Einstufung:                  {verdict}")
    print(f"Analysierte Token-Anzahl:             {ntokens}")
    print("=" * 65 + "\n")

    return {
        "criterion": crit,
        "probability": prob,
        "probability_percent": prob_pct,
        "verdict": verdict,
        "tokens": ntokens
    }

def main():
    parser = argparse.ArgumentParser(
        description="Fast-DetectGPT: Schnelle Zero-Shot Erkennung von KI-generiertem Text"
    )
    parser.add_argument(
        "--text", "-t", type=str, help="Der zu analysierende Text (in Anführungszeichen)"
    )
    parser.add_argument(
        "--file", "-f", type=str, help="Pfad zu einer Text- oder Markdown-Datei"
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
        evaluate_text(detector, args.text, title="Direkter Text")
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"[-] Datei nicht gefunden: {file_path}")
            sys.exit(1)
        content = file_path.read_text(encoding="utf-8")
        evaluate_text(detector, content, title=file_path.name)
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
                evaluate_text(detector, raw_text)
            except KeyboardInterrupt:
                print("\nProgramm beendet.")
                break

if __name__ == "__main__":
    main()
