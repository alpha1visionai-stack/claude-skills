import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_DATEI = "/opt/data/home/Documents/Finanzen/Ausgaben_2026.xlsx"
DOKUMENT_EXCEL = "/opt/data/home/Documents/Finanzen/Dokumente.xlsx"
OBSIDIAN_VAULT = "/opt/data/home/Documents/Obsidian Vault"
OBSIDIAN_BELEGE_ORDNER = os.path.join(OBSIDIAN_VAULT, "20-Areas", "Finanzen")
OBSIDIAN_DOKUMENTE_ORDNER = os.path.join(OBSIDIAN_VAULT, "30-Resources", "Dokumente")
KATEGORIEN = [
    "Burobedarf", "Software / Lizenzen", "Hardware / IT",
    "Fortbildung / Seminare", "Fachliteratur", "Reise / Verpflegung",
    "Fahrzeug / KFZ", "Telekommunikation", "Versicherung",
    "Miete / Nebenkosten", "Dienstleistung / Beratung",
    "Marketing / Werbung", "Sonstige Betriebsausgaben", "Private Ausgaben",
]
DOKUMENT_TYPEN = [
    "Zeitungsartikel", "Gebrauchsanleitung / Manual", "Anleitung / Tutorial",
    "Formular / Vordruck", "Brief / Korrespondenz", "Vertrag / Vereinbarung",
    "Notiz / Memo", "Technische Dokumentation", "Werbeunterlage / Flyer",
    "Sonstiges Dokument",
]
MWST_OPTIONS = {"19": 0.19, "7": 0.07, "0": 0.0}
