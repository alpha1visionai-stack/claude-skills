---
name: beleg-verarbeitung
description: "Beleg-Verarbeitung mit automatischer Dokumenttyp-Erkennung (Finanzbeleg vs. Zeitungsartikel etc.) -> Obsidian + Excel. TRIGGER: 'beleg', 'rechnung', 'quittung', 'scanne das', 'verarbeite beleg', 'buchung', 'parkbeleg', 'kassenbon', 'zeitungsartikel', 'dokument', 'gebrauchsanleitung', 'formular'"
---

# Beleg-Verarbeitung

Verarbeitet Belege (Fotos + PDFs) mit automatischer Dokumenttyp-Erkennung:

- **Finanzbelege** (Rechnung, Quittung, Kassenbon) -> in Ausgaben-Excel + Obsidian Finanzen
- **Dokumente** (Zeitungsartikel, Anleitung, Formular, Vertrag etc.) -> in Dokumenten-Archiv

## Funktionsweise

1. **Analyse** - Bild per Vision-LLM (GPT-4o-mini via OpenRouter) oder PDF per Textextraktion
2. **Klassifikation** - Erkennt automatisch: Finanzbeleg oder Dokumenttyp
3. **Speicherung** - Finanzbelege -> Ausgaben-Excel + Obsidian, Dokumente -> Dokumenten-Excel + Obsidian

## Voraussetzungen

```bash
python3 -m venv /opt/data/beleg_env
/opt/data/beleg_env/bin/pip install openpyxl pymupdf requests pillow
echo "OPENROUTER_API_KEY=your-key-here" >> /opt/data/.env
```

## Verwendung

```bash
/opt/data/beleg_env/bin/python3 scripts/beleg-verarbeitung.py /pfad/zum/beleg.jpg
```

## Struktur

```
beleg-verarbeitung/
  SKILL.md
  scripts/beleg-verarbeitung.py
  templates/obsidian-beleg.md
  belegsystem/config.py / beleg_parser.py / beleg_excel.py / beleg_obsidian.py
```

## Pfade in belegsystem/config.py anpassen!
