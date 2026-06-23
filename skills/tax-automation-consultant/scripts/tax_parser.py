# -*- coding: utf-8 -*-
import fitz
import json
import requests
import os
import pandas as pd
import google.generativeai as genai

# --- KONFIGURATION ---
AI_MODE = "local" # "local" oder "cloud"
OLLAMA_MODEL = "mistral-nemo" 
GEMINI_API_KEY = "DEIN_KEY_HIER" # Nur für Cloud-Modus

OLLAMA_URL = "http://localhost:11434/api/generate"
INPUT_FOLDER = "./belege" # Oder "./belege_anonym" im Cloud-Modus
OUTPUT_FILE = "steuer_erfassung.csv"

def extract_text(path):
    doc = fitz.open(path)
    return "".join([p.get_text() for p in doc])

def classify_local(text):
    prompt = (
        "Analysiere den folgenden Beleg und gib NUR ein JSON-Objekt zurück. "
        "Alle Felder sind Strings oder Zahlen, keine verschachtelten Objekte.\n\n"
        "Schema (exakt diese Felder, keine anderen):\n"
        "{\n"
        '  "datum": "TT.MM.JJJJ",\n'
        '  "betrag": 0.00,\n'
        '  "mwst": 0.00,\n'
        '  "aussteller": "Firmenname als einfacher String",\n'
        '  "kategorie": "Freiberuflich_Ausgabe"\n'
        "}\n\n"
        "WICHTIG: Ich bin Walter Krumbacher, KI-Berater, Egerländer Weg 25, 61476 Kronberg.\n"
        "Wenn ich der Rechnungssteller/Aussteller bin → Freiberuflich_Einnahme.\n"
        "Wenn ich der Rechnungsempfänger/Käufer bin → Freiberuflich_Ausgabe.\n\n"
        "Kategorie-Regeln:\n"
        "- Freiberuflich_Einnahme: ICH (Walter Krumbacher) habe die Rechnung ausgestellt und erhalte Geld\n"
        "- Freiberuflich_Ausgabe: Ich kaufe etwas oder zahle für Software, Tools, Abonnements, Hardware\n"
        "- Rente: Rentenbescheid oder Rentenzahlung\n"
        "- Abfindung: Einmalzahlung bei Kündigung/Aufhebungsvertrag\n"
        "- Sonstiges: Alles andere\n\n"
        "Beleg:\n"
        f"{text}"
    )
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False, "format": "json"}
    raw = requests.post(OLLAMA_URL, json=payload).json()['response']
    data = json.loads(raw)
    # Nur die erwarteten Felder behalten
    return {k: data.get(k, "") for k in ["datum", "betrag", "mwst", "aussteller", "kategorie"]}

def classify_cloud(text):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    resp = model.generate_content(f"Gib nur JSON zurück: {{datum, betrag, mwst, aussteller, kategorie}} für:\n{text}")
    return json.loads(resp.text.replace("```json", "").replace("```", "").strip())

def main():
    import time
    if not os.path.exists(INPUT_FOLDER): os.makedirs(INPUT_FOLDER)

    # Bereits verarbeitete Dateien laden (Resume-Funktion)
    done = set()
    results = []
    if os.path.exists(OUTPUT_FILE):
        existing = pd.read_csv(OUTPUT_FILE, encoding='utf-8-sig')
        results = existing.to_dict('records')
        done = set(existing['dateiname'].tolist())
        print(f"Setze fort: {len(done)} Belege bereits verarbeitet.")

    files = sorted([f for f in os.listdir(INPUT_FOLDER) if f.endswith(".pdf")])
    todo = [f for f in files if f not in done]
    total = len(files)
    print(f"Gesamt: {total} PDFs | Noch offen: {len(todo)}\n")

    start = time.time()
    for i, f in enumerate(todo, 1):
        elapsed = time.time() - start
        avg = elapsed / i if i > 1 else 0
        eta = avg * (len(todo) - i)
        print(f"[{len(done)+i}/{total}] {f} | ETA: {int(eta//60)}m {int(eta%60)}s")
        try:
            text = extract_text(os.path.join(INPUT_FOLDER, f))
            data = classify_local(text) if AI_MODE == "local" else classify_cloud(text)
            data['dateiname'] = f
            results.append(data)
            # Nach jedem Beleg speichern
            pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        except Exception as e:
            print(f"  FEHLER: {e}")

    print(f"\nFertig! {len(results)} Belege in {OUTPUT_FILE}")
    df = pd.DataFrame(results)
    print("\n--- Auswertung ---")
    print(df['kategorie'].value_counts().to_string())
    einnahmen = pd.to_numeric(df.loc[df['kategorie']=='Freiberuflich_Einnahme','betrag'], errors='coerce').sum()
    ausgaben  = pd.to_numeric(df.loc[df['kategorie']=='Freiberuflich_Ausgabe', 'betrag'], errors='coerce').sum()
    print(f"\nEinnahmen: {einnahmen:.2f} €")
    print(f"Ausgaben:  {ausgaben:.2f} €")
    print(f"Saldo:     {einnahmen - ausgaben:.2f} €")

if __name__ == "__main__":
    main()