# -*- coding: utf-8 -*-
import fitz  # PyMuPDF
import re
import os

# --- KONFIGURATION ---
INPUT_FOLDER = "./belege"
OUTPUT_FOLDER = "./belege_anonym"

# HIER DEINE DATEN EINTRAGEN, DIE GESCHWÄRZT WERDEN SOLLEN
STRINGS_TO_REDACT = ["Walter Krumbacher", "Egerländer Weg 25", "61476 Kronberg"]

PATTERNS = {
    "Steuernummer": r"\d{2}/\d{3}/\d{5}",
    "Steuer_ID": r"\d{11}",
    "IBAN": r"DE\d{20}",
    "Email": r"[\w\.-]+@[\w\.-]+\.\w+"
}

def redact_pdf(file_path, output_path):
    doc = fitz.open(file_path)
    count = 0
    for page in doc:
        for s in STRINGS_TO_REDACT:
            for area in page.search_for(s):
                page.add_redact_annot(area, fill=(0, 0, 0))
                count += 1
        text = page.get_text("text")
        for label, pattern in PATTERNS.items():
            for match in re.finditer(pattern, text):
                for area in page.search_for(match.group()):
                    page.add_redact_annot(area, fill=(0, 0, 0))
                    count += 1
        page.apply_redactions()
    if count > 0:
        doc.save(output_path, garbage=4, deflate=True)
        return True, count
    doc.close()
    return False, 0

def main():
    if not os.path.exists(OUTPUT_FOLDER): os.makedirs(OUTPUT_FOLDER)
    files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".pdf")]
    for f in files:
        success, n = redact_pdf(os.path.join(INPUT_FOLDER, f), os.path.join(OUTPUT_FOLDER, f))
        print(f"{'[OK]' if success else '[SKIPPED]'} {f}: {n} Schwärzungen.")

if __name__ == "__main__":
    main()