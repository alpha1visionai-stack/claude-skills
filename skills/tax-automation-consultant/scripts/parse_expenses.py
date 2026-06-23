import json
import re
import csv
import os

def parse_german_float(s):
    if not s: return 0.0
    s = s.replace('€', '').replace('EUR', '').replace('$', '').replace('USD', '').strip()
    if ',' in s and '.' in s:
        if s.rfind('.') > s.rfind(','): # 1,234.56
            s = s.replace(',', '')
        else: # 1.234,56
            s = s.replace('.', '').replace(',', '.')
    elif ',' in s:
        # If there's only one comma, it could be decimal or thousand separator.
        # In German it's decimal.
        s = s.replace(',', '.')
    
    try:
        s = re.sub(r'[^\d.]', '', s)
        return float(s)
    except:
        return 0.0

def format_german_float(f):
    return "{:.2f}".format(f).replace('.', ',')

def categorize(text, filename):
    text = text.lower()
    filename = filename.lower()
    
    if "amazon" in text or "amazon" in filename:
        if any(x in text for x in ["monitor", "ipad", "laptop", "omen", "netzteil", "ssd", "usb", "hub", "kabel", "tenda", "webcam", "router", "power bank", "magsafe", "induktion", "picogo", "displayport"]):
            return "EDV-Kosten"
        if any(x in text for x in ["bürostuhl"]):
            return "Werkzeuge und Kleingeräte"
        if any(x in text for x in ["collegeblock", "ordner", "notizblock", "hülle", "pencil"]):
            return "Bürobedarf"
    
    if any(x in text or x in filename for x in ["hetzner", "google", "openrouter", "apple", "samsung", "tenda", "ugreen", "baseus", "benfei", "fintie", "logitech", "lg electronics", "ssd", "usb", "hub", "kabel", "router"]):
        return "EDV-Kosten"
    
    if "udemy" in text:
        return "Fortbildungskosten"
    
    if "quicksteuer" in text:
        return "Rechts- und Beratungskosten"
    
    if "sixt" in text:
        return "Reisekosten"
    
    if "sepa" in text:
        return None
    
    return "Sonstige Betriebsausgaben"

def normalize_date(date_str):
    if not date_str: return "01.01.2025"
    date_str = date_str.lower().strip()
    
    # DD.MM.YYYY
    m = re.match(r'(\d{1,2})[\./](\d{1,2})[\./](\d{4})', date_str)
    if m:
        return f"{int(m.group(1)):02d}.{int(m.group(2)):02d}.{m.group(3)}"
    
    # Month DD, YYYY (e.g. February 1, 2025)
    months_map = {
        "jan": "01", "feb": "02", "mär": "03", "apr": "04", "mai": "05", "jun": "06",
        "jul": "07", "aug": "08", "sep": "09", "okt": "10", "nov": "11", "dez": "12",
        "januar": "01", "februar": "02", "märz": "03", "april": "04", "mai": "05", "juni": "06",
        "juli": "07", "august": "08", "september": "09", "oktober": "10", "november": "11", "dezember": "12"
    }
    
    # Try Month DD, YYYY
    m = re.search(r'([a-z]+)\s+(\d{1,2}),?\s+(\d{4})', date_str)
    if m:
        month_str = m.group(1)
        day = int(m.group(2))
        year = m.group(3)
        for k, v in months_map.items():
            if month_str.startswith(k):
                return f"{day:02d}.{v}.{year}"

    # Try DD. Month YYYY
    m = re.search(r'(\d{1,2})\.?\s*([a-zä]+)\.?\s*(\d{4})', date_str)
    if m:
        day = int(m.group(1))
        month_str = m.group(2)
        year = m.group(3)
        for k, v in months_map.items():
            if month_str.startswith(k):
                return f"{day:02d}.{v}.{year}"
    
    return date_str

def extract_data(filename, text):
    if "sepa-mandat" in filename.lower() or "sepa mandat" in text.lower():
        return None
    
    # Try to find date
    date = ""
    # Look for Month DD, YYYY or DD. Month YYYY
    months = ["januar", "februar", "märz", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "dezember", 
              "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december",
              "jan", "feb", "mär", "apr", "mai", "jun", "jul", "aug", "sep", "okt", "nov", "dez"]
    
    date_patterns = [
        r'(\d{1,2}[\./]\d{1,2}[\./]\d{4})',
        r'(([a-z]+)\s+\d{1,2},?\s+\d{4})',
        r'(\d{1,2}\.?\s+([a-zä]+)\.?\s+\d{4})'
    ]
    
    for p in date_patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            date = m.group(1)
            break
    
    date = normalize_date(date)

    desc = filename.replace('.pdf', '')
    
    gross = 0.0
    net = 0.0
    tax = 0.0

    # Amounts
    # Look for symbols: €, EUR, $, USD
    amounts = re.findall(r'([\$€]|EUR|USD)\s*([\d,.]+)', text)
    amounts += re.findall(r'([\d,.]+)\s*([\$€]|EUR|USD)', text)
    
    # Specific logic for common invoices
    if "amazon" in text.lower():
        m_gross = re.search(r'(Gesamtpreis|Zahlbetrag|Gesamtsumme)\s*[:\n\s]*([\d,.]+)\s?€', text, re.IGNORECASE)
        if m_gross: gross = parse_german_float(m_gross.group(2))
    elif "hetzner" in text.lower():
        m = re.search(r'Zu zahlender Betrag:\s+([\d,.]+)\s?€', text)
        if m: gross = parse_german_float(m.group(1))
    elif "google" in text.lower():
        m = re.search(r'Gesamtsumme in EUR\n([\d,.]+)\s*€\n([\d,.]+)\s*€\n([\d,.]+)\s*€', text)
        if m: 
            gross = parse_german_float(m.group(3))
            net = parse_german_float(m.group(1))
            tax = parse_german_float(m.group(2))
        else:
            m2 = re.search(r'Gesamtsumme in EUR\s+([\d,.]+)\s*€', text)
            if m2: gross = parse_german_float(m2.group(1))

    if gross == 0:
        parsed_amounts = []
        for a in amounts:
            val = parse_german_float(a[0] if re.match(r'[\d,.]+', a[0]) else a[1])
            parsed_amounts.append(val)
        if parsed_amounts:
            gross = max(parsed_amounts)

    if net == 0 and gross > 0:
        # Check for tax line
        m_tax = re.search(r'(USt\.?|MwSt\.?|Umsatzsteuer)\s*(\(\d+\%\))?\s*[:\s]*([\d,.]+)\s?[\$€]', text, re.IGNORECASE)
        if m_tax:
            tax = parse_german_float(m_tax.group(3))
            net = round(gross - tax, 2)
        else:
            net = round(gross / 1.19, 2)
            tax = round(gross - net, 2)

    cat = categorize(text, filename)
    if not cat: return None

    return {
        "Datum": date,
        "Kategorie": cat,
        "Text der Ausgabe": desc,
        "Nettobetrag": net,
        "MwSt": tax,
        "Bruttobetrag": gross
    }

def main():
    with open("temp_extracted_text.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    rows = []
    for filename, text in data.items():
        entry = extract_data(filename, text)
        if entry:
            rows.append(entry)
    
    def date_key(d):
        parts = d["Datum"].split('.')
        if len(parts) == 3:
            try:
                return f"{int(parts[2]):04d}-{int(parts[1]):02d}-{int(parts[0]):02d}"
            except:
                pass
        return "0000-00-00"
    
    rows.sort(key=date_key)

    output_path = r"D:\OneDrive\Dokumente\KI-Beratung\2025\belege_anonym Ausgaben\Ausgabenübersicht_2025.csv"
    with open(output_path, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Datum", "Kategorie", "Text der Ausgabe", "Nettobetrag", "MwSt", "Bruttobetrag"])
        for r in rows:
            writer.writerow([
                r["Datum"],
                r["Kategorie"],
                r["Text der Ausgabe"],
                format_german_float(r["Nettobetrag"]),
                format_german_float(r["MwSt"]),
                format_german_float(r["Bruttobetrag"])
            ])
    print(f"Created CSV with {len(rows)} entries.")

if __name__ == "__main__":
    main()
