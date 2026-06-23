import os
import json
from pypdf import PdfReader

def extract_text_from_pdfs(directory):
    results = {}
    for filename in os.listdir(directory):
        if filename.lower().endswith(".pdf"):
            path = os.path.join(directory, filename)
            try:
                reader = PdfReader(path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                results[filename] = text
            except Exception as e:
                results[filename] = f"Error: {str(e)}"
    return results

if __name__ == "__main__":
    dir_path = r"D:\OneDrive\Dokumente\KI-Beratung\2025\belege_anonym Ausgaben"
    data = extract_text_from_pdfs(dir_path)
    # Output to a file because it might be too large for stdout
    with open("temp_extracted_text.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Extracted text from {len(data)} files.")
