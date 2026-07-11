#!/usr/bin/env python3
import sys, os, json, shutil
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL_DIR, "belegsystem"))
from beleg_parser import verarbeite_beleg
from beleg_excel import beleg_hinzufuegen
from beleg_obsidian import beleg_notiz_schreiben, _generiere_dateiname
from config import DOKUMENT_EXCEL, OBSIDIAN_DOKUMENTE_ORDNER

def main():
    if len(sys.argv) < 2:
        print("Nutzung: python3 beleg-verarbeitung.py /pfad/zum/beleg.pdf|.jpg")
        sys.exit(1)
    path = os.path.abspath(sys.argv[1])
    if not os.path.exists(path):
        print(f"Datei nicht gefunden: {path}")
        sys.exit(1)
    print(f"Verarbeite: {path}")
    daten = verarbeite_beleg(path)
    print(json.dumps(daten, ensure_ascii=False, indent=2))
    if daten.get("dokumenttyp") == "Finanzbeleg":
        obs = beleg_notiz_schreiben(daten)
        excel = beleg_hinzufuegen(daten)
    else:
        print(f"Dokumenttyp: {daten.get('dokumenttyp','?')} -> Dokumente-Archiv")
        obs = beleg_notiz_schreiben(daten, output_ordner=OBSIDIAN_DOKUMENTE_ORDNER)
        excel = beleg_hinzufuegen(daten, excel_path=DOKUMENT_EXCEL)
    print(f"Obsidian: {obs}")
    obs_ordner = os.path.dirname(obs)
    sprechend = _generiere_dateiname(daten)
    orig_ext = os.path.splitext(path)[1]
    ziel = os.path.join(obs_ordner, f"{sprechend}{orig_ext}")
    if path != ziel and not os.path.exists(ziel):
        try:
            shutil.copy2(path, ziel)
            print(f"Original kopiert: {ziel}")
        except:
            pass
    print(f"Excel: {excel}")

if __name__ == "__main__":
    main()
