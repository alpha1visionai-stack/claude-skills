import os
import shutil
import abc
import argparse
from typing import Dict, List, Optional

class DocumentConsolidator:
    def __init__(self, target_dir: str):
        self.target_dir = target_dir
        self.originals_dir = os.path.join(target_dir, "Originale")
        self.standard_files = {
            "Angebote_Konzepte.md": ["angebot", "konzept", "pitch", "vorschlag"],
            "Analysen_UseCases.md": ["analyse", "use case", "fallstudie", "untersuchung"],
            "Automatisierung_n8n.md": ["n8n", "workflow", "automatisierung", "flow"],
            "Kalkulationen_Kosten.md": ["kosten", "kalkulation", "budget", "preis", "angebot", "rechnung"],
            "Meetings_Protokolle.md": ["protokoll", "meeting", "besprechung", "notizen"],
            "Manifest_Vision.md": ["vision", "manifest", "strategie", "ziele"],
            "Compliance_GDPR.md": ["compliance", "gdpr", "datenschutz", "rechtlich"],
            "system_prompts.md": ["prompt", "persona", "instruktion", "system prompt", "/cmd"]
        }

    def ensure_structure(self):
        if not os.path.exists(self.originals_dir):
            os.makedirs(self.originals_dir)

    def extract_text(self, file_path: str) -> str:
        # Use markitdown via CLI (assuming it's installed as per previous steps)
        import subprocess
        try:
            result = subprocess.run(["python", "-m", "markitdown", file_path], capture_output=True, text=True, check=True)
            return result.stdout
        except Exception as e:
            return f"Error extracting {file_path}: {e}"

    def categorize_content(self, text: str, filename: str) -> str:
        # Simple heuristic mapping based on keywords in content or filename
        combined = (text[:1000] + filename).lower()
        for md_file, keywords in self.standard_files.items():
            if any(k in combined for k in keywords):
                return md_file
        return "Angebote_Konzepte.md" # Default

    def process_file(self, file_path: str):
        if not os.path.isfile(file_path):
            return

        filename = os.path.basename(file_path)
        if filename.endswith(('.pdf', '.docx', '.xlsx', '.pptx', '.gdoc', '.gsheet')):
            print(f"Processing: {filename}")

            # 1. Extraction
            content = self.extract_text(file_path)

            # 2. Categorization
            target_md = self.categorize_content(content, filename)
            target_path = os.path.join(self.target_dir, target_md)

            # 3. Merging (Appending)
            with open(target_path, "a", encoding="utf-8") as f:
                f.write(f"\n\n--- Quelle: {filename} ---\n\n")
                f.write(content)

            # 4. Archiving
            shutil.move(file_path, os.path.join(self.originals_dir, filename))
            print(f"Consolidated into {target_md} and archived {filename}")

def main():
    parser = argparse.ArgumentParser(description="Consolidate documents into categorized markdown files.")
    parser. Rose = parser.add_argument("path", help="Path to the document or directory to process")
    args = parser.parse_args()

    path = os.path.abspath(args.path)
    if os.path.isdir(path):
        consolidator = DocumentConsolidator(path)
        consolidator.ensure_structure()
        for f in os.listdir(path):
            if f != "Originale":
                consolidator.process_file(os.path.join(path, f))
    else:
        consolidator = DocumentConsolidator(os.path.dirname(path))
        consolidator.ensure_structure()
        consolidator.process_file(path)

if __name__ == "__main__":
    main()
