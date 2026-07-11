#!/usr/bin/env python3
"""
beleg_obsidian.py — Schreibt Beleg-Notizen in Obsidian Vault.

Pro Beleg wird eine Markdown-Datei im entsprechenden Ordner angelegt.
Der Dateiname wird automatisch aus der Analyse generiert (sprechender Name).
"""

import os
import sys
import json
import re
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import OBSIDIAN_VAULT, OBSIDIAN_BELEGE_ORDNER, OBSIDIAN_DOKUMENTE_ORDNER


def _generiere_dateiname(beleg: dict) -> str:
    """Generiert einen sprechenden Dateinamen aus den Belegdaten."""
    datum = str(beleg.get("datum", datetime.now().strftime("%Y-%m-%d")))
    dokumenttyp = beleg.get("dokumenttyp", "Finanzbeleg")

    # Namensquelle wählen: bei Finanzbeleg → Rechnungssteller, sonst → Bezeichnung
    if dokumenttyp == "Finanzbeleg":
        name_roh = beleg.get("rechnungssteller", "")
        fallback = beleg.get("bezeichnung", "Beleg")
    else:
        name_roh = beleg.get("bezeichnung", "")
        fallback = beleg.get("rechnungssteller", dokumenttyp)

    if not name_roh or name_roh.strip() == "":
        name_roh = fallback
    if not name_roh or name_roh.strip() == "":
        name_roh = "Unbekannt"

    # Bereinigen: nur alphanumerisch, Bindestriche und Unterstriche
    name = re.sub(r'[^\w\s-]', '', name_roh, flags=re.UNICODE)
    name = re.sub(r'[_\s]+', '_', name.strip())
    name = name.strip('_')[:60]

    return f"{datum}_{name}"


def beleg_notiz_schreiben(beleg: dict, output_ordner: str = None) -> str:
    """
    Schreibt eine Beleg-Notiz im Obsidian Vault.
    - beleg: Dict mit den Feldern
    - output_ordner: Optional anderer Ordner (z.B. 30-Resources/Dokumente/)
    Gibt den Dateipfad zurück.
    """
    ordner = output_ordner or OBSIDIAN_BELEGE_ORDNER
    datum = str(beleg.get("datum", datetime.now().strftime("%Y-%m-%d")))
    dokumenttyp = beleg.get("dokumenttyp", "Finanzbeleg")
    rechnungssteller = beleg.get("rechnungssteller", "Unbekannt")
    brutto = float(beleg.get("brutto", 0))
    kategorie = beleg.get("kategorie", "Sonstige Betriebsausgaben")
    bezeichnung = beleg.get("bezeichnung", "")
    dateiname_orig = beleg.get("_dateiname", "beleg")

    # Sprechender Dateiname
    safe_name = _generiere_dateiname(beleg)
    notiz_name = f"{safe_name}.md"
    notiz_pfad = os.path.join(ordner, notiz_name)

    # Verzeichnis anlegen
    os.makedirs(ordner, exist_ok=True)

    # Dokumenttyp-spezifischer Titel
    if dokumenttyp == "Finanzbeleg":
        titel = f"Finanzbeleg: {rechnungssteller}"
    else:
        titel = f"{dokumenttyp}: {bezeichnung or rechnungssteller}"

    # Frontmatter
    frontmatter = f"""---
datum: {datum}
dokumenttyp: "{dokumenttyp}"
kategorie: "{kategorie}"
rechnungssteller: "{rechnungssteller}"
bezeichnung: "{bezeichnung}"
netto: {float(beleg.get('netto', 0)):.2f}
mwst_satz: "{beleg.get('mwst_satz', '19')}"
mwst_betrag: {float(beleg.get('mwst_betrag', 0)):.2f}
brutto: {brutto:.2f}
waehrung: "{beleg.get('waehrung', 'EUR')}"
belegnummer: "{beleg.get('belegnummer', '')}"
eingereicht_am: "{beleg.get('_verarbeitet_am', datetime.now().isoformat())}"
status: erfasst
tags: [{dokumenttyp.lower().replace(' ', '-')}]
---
"""

    # Body
    erklaerung = beleg.get("erklaerung", "")
    belegnummer = beleg.get("belegnummer", "")
    netto = float(beleg.get("netto", 0))
    mwst_satz = beleg.get("mwst_satz", "19")
    mwst_betrag = float(beleg.get("mwst_betrag", 0))

    if dokumenttyp == "Finanzbeleg":
        belegnummer_zeile = f"| **Belegnummer** | {belegnummer} |\n" if belegnummer else ""

        body = f"""# {titel}

## Rechnungsdetails

| Feld | Wert |
|------|------|
| **Datum** | {datum} |
| **Dokumenttyp** | {dokumenttyp} |
| **Kategorie** | {kategorie} |
| **Rechnungssteller** | {rechnungssteller} |
| **Bezeichnung** | {bezeichnung} |
| **Nettobetrag** | {netto:.2f} EUR |
| **MwSt-Satz** | {mwst_satz}% |
| **MwSt-Betrag** | {mwst_betrag:.2f} EUR |
| **Bruttobetrag** | {brutto:.2f} EUR |
{belegnummer_zeile}| **Währung** | {beleg.get('waehrung', 'EUR')} |

## Belegdatei
- Originaldatei: `{dateiname_orig}`

## Analyse
{erklaerung if erklaerung else "*Automatisch erfasst.*"}
"""
    else:
        body = f"""# {titel}

## Dokumentdetails

| Feld | Wert |
|------|------|
| **Datum** | {datum} |
| **Dokumenttyp** | {dokumenttyp} |
| **Quelle / Autor** | {rechnungssteller} |
| **Titel / Beschreibung** | {bezeichnung} |

## Belegdatei
- Originaldatei: `{dateiname_orig}`

## Analyse
{erklaerung if erklaerung else "*Automatisch erfasst.*"}
"""

    with open(notiz_pfad, "w", encoding="utf-8") as f:
        f.write(frontmatter + body)

    print(f"📝 Obsidian-Notiz geschrieben: {notiz_pfad}")
    return notiz_pfad


# ─── CLI ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--add":
        beleg_json = sys.stdin.read()
        beleg = json.loads(beleg_json)
        pfad = beleg_notiz_schreiben(beleg)
        print(pfad)
    elif len(sys.argv) > 1 and sys.argv[1] == "--dateiname":
        beleg_json = sys.stdin.read()
        beleg = json.loads(beleg_json)
        print(_generiere_dateiname(beleg))
    else:
        print(f"Verwendung: echo '<json>' | python beleg_obsidian.py --add")
        print(f"  oder:      echo '<json>' | python beleg_obsidian.py --dateiname")
        print(f"Obsidian-Ordner Finanzen: {OBSIDIAN_BELEGE_ORDNER}")
        print(f"Obsidian-Ordner Dokumente: {OBSIDIAN_DOKUMENTE_ORDNER}")