---
name: tax-automation-consultant
description: Automatisierte Steuererfassung für Berater und Freiberufler (EÜR/USt). Analysiert Belege, berechnet Pauschalen (Arbeitszimmer, KFZ, Telefon) und generiert PDF-Berichte.
---

# Tax Automation Consultant

Dieser Skill automatisiert den jährlichen Steuererfassungs-Prozess für die Einnahmen-Überschuss-Rechnung (EÜR).

## Workflow

### 1. Vorbereitung
- Stelle sicher, dass alle Belege des Jahres in einem Ordner (z.B. `belege_anonym/`) liegen.
- Die erlaubten Kategorien befinden sich in `references/kategorien.txt`.

### 2. Beleg-Analyse
Verwende die Skripte `scripts/tax_parser.py` oder `scripts/parse_expenses.py`, um die PDFs zu analysieren und eine CSV-Übersicht zu erstellen.
- **Input:** PDF-Belege.
- **Output:** `Ausgabenübersicht_<Jahr>.csv`.

### 3. Pauschalberechnung
Führe `scripts/pauschalen_rechner.py` aus, um die anteiligen Kosten für das Arbeitszimmer und andere Pauschalen zu berechnen.
**Wichtig:** Frage den Nutzer nach den aktuellen Basisdaten für das neue Jahr:
- Anschaffungskosten Haus & Restschuld (Zinsen).
- Wohnfläche & Arbeitszimmer-Fläche.
- Jährliche Gesamtkosten für Strom, Heizung (Erdgas), Wasser, Müll, Versicherung, Grundsteuer.
- Telefonkosten & betrieblicher Anteil.
- KFZ-Fahrten (Strecke & Häufigkeit).

### 4. Berichterstellung
Generiere die finalen Berichte für QuickSteuer:
- `scripts/generate_pdf_report.py`: Erstellt den kategorisierten PDF-Bericht der Belege mit Seitenumbrüchen.
- `scripts/generate_pauschal_pdf.py`: Erstellt die QuickSteuer-Eingabehilfe mit den 10% anteiligen Kosten.

## Wichtige Konzepte
- **Ist-Versteuerung & Zuflussprinzip:** Erinnere den Nutzer daran, dass nur Geldeingänge im jeweiligen Kalenderjahr zählen (wichtig bei Rechnungen zum Jahreswechsel).
- **10-Tages-Regel:** Prüfe regelmäßig wiederkehrende Zahlungen rund um den Jahreswechsel.
- **Abschreibung (AfA):** Berücksichtige Büromöbel und Gebäude-AfA (Nutzungsdauer beachten).

## Scripts
- `tax_workflow_master.py`: Koordiniert den gesamten Ablauf.
- `pdf_redactor.py`: Zum Anonymisieren sensibler Daten in Belegen.
