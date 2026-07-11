#!/usr/bin/env python3
"""
beleg_parser.py — Extrahiert Text aus PDFs/Bildern und analysiert Belegdaten.

Funktionsweise:
1. PDF → pymupdf Textextraktion
2. Bild (JPG/PNG) → pymupdf-Darstellung → LLM-Analyse
3. Rohtext → LLM-gestützte Strukturierung in Belegfelder
"""

import os
import sys
import json
import re
import tempfile
import subprocess
import requests
from datetime import datetime
from pathlib import Path

# Projekt-Import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import KATEGORIEN, MWST_OPTIONS

# ─── 1. PDF-Textextraktion ───────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extrahiert Text aus einer PDF-Datei via pymupdf."""
    try:
        import fitz  # pymupdf
    except ImportError:
        print("FEHLER: pymupdf nicht installiert. Bitte: pip install pymupdf", file=sys.stderr)
        sys.exit(1)

    doc = fitz.open(pdf_path)
    text_parts = []
    for page_num, page in enumerate(doc):
        page_text = page.get_text("text")
        if page_text.strip():
            text_parts.append(f"--- Seite {page_num + 1} ---\n{page_text}")
    doc.close()

    full_text = "\n\n".join(text_parts)
    return full_text.strip()


def analyze_image_directly(image_path: str) -> dict:
    """
    Analysiert ein Beleg-Foto direkt per Vision-LLM (GPT-4o-mini).
    Extrahiert strukturierte Daten in einem Schritt — kein Textextraktions-Zwischenschritt.
    """
    import base64

    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    # OpenRouter API-Key
    key = ""
    for env_file in ["/opt/data/.env", "/opt/data/.env.bak-20260628T071324Z"]:
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    if line.startswith("OPENROUTER_API_KEY="):
                        key = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not key:
        return {"dokumenttyp": "Sonstiges Dokument", "kategorie": "Sonstige Betriebsausgaben", "erklaerung": "Kein API-Key"}

    from config import KATEGORIEN, DOKUMENT_TYPEN
    kats = "\n".join(f"  - {k}" for k in KATEGORIEN)
    doks = "\n".join(f"  - {d}" for d in DOKUMENT_TYPEN)

    prompt = f"""Du siehst ein Foto eines Dokuments.
Bestimme zuerst den DOKUMENTTYP:

    IST DAS EIN FINANZBELEG? (Rechnung, Quittung, Kassenbon, Zahlungsbeleg, Mahnung, Spendenquittung)
    - Ja → dokumenttyp = "Finanzbeleg", dann extrahiere alle Finanzdaten
    - Nein → dokumenttyp ist einer der folgenden Dokumenttypen:
    {doks}

    Wähle GENAU EINE Kategorie (nur bei Finanzbeleg relevant):
    {kats}

    Antworte NUR als JSON (kein Präfix, kein Markdown):
    {{"dokumenttyp": "Finanzbeleg oder einer der Dokumenttypen oben",
    "datum": "YYYY-MM-DD", "kategorie": "... (nur bei Finanzbeleg)",
    "rechnungssteller": "...", "bezeichnung": "...",
    "netto": 0.00, "mwst_satz": "19", "mwst_betrag": 0.00,
    "brutto": 0.00, "waehrung": "EUR", "belegnummer": "",
    "erklaerung": "Kurze Beschreibung des Dokuments"}}

    Regeln:
    - dokumenttyp ist PFLICHTFELD — entweder "Finanzbeleg" oder einer aus der Dokumentliste oben
    - datum: YYYY-MM-DD (Erstellungsdatum des Dokuments, bei Zeitungen: Datum der Ausgabe)
    - Bei Finanzbeleg: netto + mwst_betrag = brutto
    - Bei Finanzbeleg mit nur Brutto: netto = brutto / 1.19
    - mwst_satz als String (z.B. "19")
    - rechnungssteller = Absender/Herausgeber/Quelle des Dokuments
    - bezeichnung = Titel oder Kurzbeschreibung
    - Netto/MwSt/Brutto bei Nicht-Finanzdokumenten auf 0.00 setzen, waehrung = ""
    - belegnummer bei Nicht-Finanzdokumenten leer lassen"""

    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [{"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                ]}],
                "max_tokens": 2000,
                "temperature": 0.05,
            },
            timeout=30,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()
        # JSON parsen
        import re
        content = re.sub(r'```(?:json)?\s*', '', content).strip()
        start = content.find('{')
        end = content.rfind('}')
        if start >= 0 and end > start:
            content = content[start:end + 1]
        return json.loads(content)
    except Exception as e:
        print(f"⚠️  Vision-LLM Fehler: {e}", file=sys.stderr)
        return {"dokumenttyp": "Sonstiges Dokument", "kategorie": "Sonstige Betriebsausgaben", "erklaerung": f"Vision-Fehler: {e}"}


# ─── 2. LLM-Analyse (via Subprozess / API-Aufruf) ──────────────────────

def analyze_receipt_text(rohtext: str, dateiname: str = "") -> dict:
    """
    Analysiert den Rohtext eines Belegs und strukturiert die Daten.
    Gibt ein Dict zurück: datum, kategorie, rechnungssteller, bezeichnung,
    netto, mwst_satz, mwst_betrag, brutto, waehrung, belegnummer.
    """
    from config import KATEGORIEN, DOKUMENT_TYPEN
    kategorien_text = "\n".join(f"  - {k}" for k in KATEGORIEN)
    dokumente_text = "\n".join(f"  - {d}" for d in DOKUMENT_TYPEN)

    prompt = f"""Du bist ein Dokument-Analyse-Assistent. Analysiere den folgenden Text und bestimme zuerst den DOKUMENTTYP.

Beleg-Dateiname: {dateiname}

ROHTEXT:
```
{rohtext[:8000]}
```

Aufgabe:
1. Bestimme den DOKUMENTTYP:
   - Ist das ein FINANZBELEG? (Rechnung, Quittung, Kassenbon, Zahlungsbeleg, Mahnung)
   - Sonst: einer der Dokumenttypen aus der Liste unten
2. Wenn Finanzbeleg: extrahiere alle Finanzdaten und wähle Kategorie
3. Wenn Nicht-Finanzdokument: Netto/MwSt/Brutto auf 0.00 setzen

Wähle die Kategorie AUS SCHLIESSLICH aus dieser Liste (nur bei Finanzbeleg):
{kategorien_text}

Dokumenttypen für Nicht-Finanzdokumente:
{dokumente_text}

Antworte AUSSCHLIESSLICH im folgenden JSON-Format (kein Präfix, kein Suffix, keine Markdown-Blöcke — nur reines JSON):

{{
    "dokumenttyp": "Finanzbeleg oder einer der Dokumenttypen",
    "datum": "YYYY-MM-DD",
    "kategorie": "aus der Kategorieliste (nur bei Finanzbeleg)",
    "rechnungssteller": "Firmenname / Herausgeber / Quelle",
    "bezeichnung": "Titel oder Kurzbeschreibung",
    "netto": 0.00,
    "mwst_satz": "19",
    "mwst_betrag": 0.00,
    "brutto": 0.00,
    "waehrung": "EUR",
    "belegnummer": "",
    "erklaerung": "Kurze Erklärung, worum es sich handelt"
}}

Wichtige Regeln:
- dokumenttyp ist PFLICHTFELD — entweder "Finanzbeleg" oder einer aus der Dokumentliste
- Bei Finanzbeleg: Netto + MwSt = Brutto
- Bei Finanzbeleg mit nur Brutto: Netto = Brutto / (1 + mwst_satz/100)
- Standard-MwSt in Deutschland: 19% (oder 7% für Lebensmittel, Bücher, etc.)
- Bei Nicht-Finanzdokument: netto=mwst_betrag=brutto=0.00, waehrung="", belegnummer=""
- Beträge immer mit 2 Nachkommastellen
- Datum im Format YYYY-MM-DD
- Wenn kein Datum ersichtlich: nutze heutiges Datum {datetime.now().strftime("%Y-%m-%d")}"""

    # LLM via Hermes CLI oder openrouter aufrufen
    result = _call_llm(prompt)
    return _parse_llm_response(result)


def _call_llm(prompt: str, max_retries: int = 3) -> str:
    """Ruft ein LLM über die OpenRouter API auf (DeepSeek V4 Flash)."""
    # OpenRouter API-Key
    key = ""
    for env_file in ["/opt/data/.env", "/opt/data/.env.bak-20260628T071324Z"]:
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    if line.startswith("OPENROUTER_API_KEY="):
                        key = line.split("=", 1)[1].strip().strip('"').strip("'")

    if not key:
        raise RuntimeError("OPENROUTER_API_KEY nicht gefunden")

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://hermes-agent.local",
    }
    payload = {
        "model": "deepseek/deepseek-v4-flash",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 2000,
    }

    for attempt in range(max_retries):
        try:
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers, json=payload, timeout=60,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            if attempt < max_retries - 1:
                continue
            raise RuntimeError(f"LLM-Aufruf fehlgeschlagen: {e}")

    raise RuntimeError("LLM-Aufruf fehlgeschlagen nach allen Versuchen")


def _parse_llm_response(response: str) -> dict:
    """Parst die JSON-Antwort des LLM."""
    # Entferne mögliche Markdown-Blöcke
    response = re.sub(r'```(?:json)?\s*', '', response)
    response = response.strip()

    # Finde das erste { und letzte }
    start = response.find('{')
    end = response.rfind('}')
    if start >= 0 and end > start:
        response = response[start:end + 1]

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        # Fallback: versuche, mit regex zu parsen
        data = _fallback_parse(response)

    # Datentypen normalisieren
    for field in ["netto", "mwst_betrag", "brutto"]:
        if field in data and data[field] is not None:
            try:
                data[field] = round(float(str(data[field]).replace(",", ".").replace("€", "").replace("EUR", "").strip()), 2)
            except (ValueError, TypeError):
                data[field] = 0.0

    if "mwst_satz" in data and data["mwst_satz"] is not None:
        mwst_str = str(data["mwst_satz"]).replace("%", "").strip()
        if mwst_str in MWST_OPTIONS:
            data["mwst_satz"] = mwst_str
        else:
            data["mwst_satz"] = "19"

    return data


def _fallback_parse(text: str) -> dict:
    """Fallback: Regex-basierte Extraktion wenn JSON fehlschlägt."""
    data = {
        "dokumenttyp": "Finanzbeleg",
        "datum": "",
        "kategorie": "Sonstige Betriebsausgaben",
        "rechnungssteller": "",
        "bezeichnung": "",
        "netto": 0.0,
        "mwst_satz": "19",
        "mwst_betrag": 0.0,
        "brutto": 0.0,
        "waehrung": "EUR",
        "belegnummer": "",
        "erklaerung": "Automatisch extrahiert (Fallback)"
    }

    patterns = {
        "datum": r'"datum"\s*:\s*"(\d{4}-\d{2}-\d{2})"',
        "rechnungssteller": r'"rechnungssteller"\s*:\s*"([^"]+)"',
        "bezeichnung": r'"bezeichnung"\s*:\s*"([^"]+)"',
        "netto": r'"netto"\s*:\s*([\d.,]+)',
        "brutto": r'"brutto"\s*:\s*([\d.,]+)',
        "mwst_satz": r'"mwst_satz"\s*:\s*"([^"]+)"',
        "kategorie": r'"kategorie"\s*:\s*"([^"]+)"',
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            val = match.group(1)
            if key in ("netto", "brutto"):
                try:
                    data[key] = round(float(val.replace(",", ".")), 2)
                except ValueError:
                    pass
            else:
                data[key] = val

    return data


# ─── 3. Hauptfunktion ────────────────────────────────────────────────────

def verarbeite_beleg(dateipfad: str) -> dict:
    """
    Hauptfunktion: Nimmt einen Dateipfad (PDF oder Bild), extrahiert Text
    und analysiert den Beleg.
    Gibt ein Dict mit allen Belegdaten zurück.
    """
    dateipfad = str(dateipfad)
    dateiname = os.path.basename(dateipfad)
    ext = os.path.splitext(dateiname)[1].lower()

    print(f"📄 Verarbeite: {dateiname}")

    # Je nach Dateityp: Bilder direkt per Vision, PDFs via Text + Analyse
    if ext == ".pdf":
        text = extract_text_from_pdf(dateipfad)
        if not text.strip():
            print("⚠️  Kein Text aus dem PDF extrahierbar.", file=sys.stderr)
            return {
                "dokumenttyp": "Sonstiges Dokument",
                "datum": datetime.now().strftime("%Y-%m-%d"),
                "kategorie": "Sonstige Betriebsausgaben",
                "rechnungssteller": dateiname.replace(".pdf", "").replace("_", " ").title(),
                "bezeichnung": "PDF ohne extrahierbaren Text",
                "netto": 0.0, "mwst_satz": "19", "mwst_betrag": 0.0, "brutto": 0.0,
                "waehrung": "EUR", "belegnummer": "",
                "erklaerung": "Kein Text aus PDF extrahierbar — gescanntes PDF?",
                "_dateiname": dateiname, "_dateipfad": dateipfad,
            }
        print("🔍 Analysiere Belegdaten...")
        daten = analyze_receipt_text(text, dateiname)

    elif ext in (".jpg", ".jpeg", ".png", ".webp"):
        print("👁️  Bild via Vision-LLM analysieren...")
        daten = analyze_image_directly(dateipfad)
        # Felder normalisieren
        for f in ["netto", "mwst_betrag", "brutto"]:
            if f in daten and daten[f] is not None:
                try:
                    daten[f] = round(float(str(daten[f]).replace(",", ".")), 2)
                except (ValueError, TypeError):
                    daten[f] = 0.0

    else:
        raise ValueError(f"Nicht unterstütztes Format: {ext}")

    # Metadaten ergänzen & dokumenttyp normalisieren
    daten["_dateiname"] = dateiname
    daten["_dateipfad"] = dateipfad
    daten["_verarbeitet_am"] = datetime.now().isoformat()
    if "dokumenttyp" not in daten or not daten.get("dokumenttyp"):
        daten["dokumenttyp"] = "Finanzbeleg"

    typ = daten.get("dokumenttyp", "Finanzbeleg")
    if typ == "Finanzbeleg":
        print(f"✅ {typ}: {daten.get('rechnungssteller', '?')} — {daten.get('brutto', 0):.2f} EUR")
    else:
        print(f"✅ {typ}: {daten.get('bezeichnung', '?')} ({daten.get('rechnungssteller', '?')})")
    return daten


# ─── CLI ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Verwendung: python beleg_parser.py <datei.pdf|datei.jpg>", file=sys.stderr)
        sys.exit(1)

    dateipfad = sys.argv[1]
    if not os.path.exists(dateipfad):
        print(f"Datei nicht gefunden: {dateipfad}", file=sys.stderr)
        sys.exit(1)

    daten = verarbeite_beleg(dateipfad)
    print(json.dumps(daten, ensure_ascii=False, indent=2))