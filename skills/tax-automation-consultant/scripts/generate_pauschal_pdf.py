import pandas as pd
from fpdf import FPDF
import os

# Pfade
csv_path = r'D:\OneDrive\Dokumente\KI-Beratung\2025\steuer_erfassung.csv'
pdf_path = r'D:\OneDrive\Dokumente\KI-Beratung\2025\Berichte\Pauschalberechnung_2025.pdf'

def float_to_german_num(val):
    return f"{val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Basisdaten
basis = {
    "Wohnfläche Gesamt": "150 m²",
    "Fläche Arbeitszimmer": "15 m²",
    "Absetzbarer Anteil": "10,00%",
    "Anschaffungskosten Haus": "550.000,00 EUR",
    "Gebäude-AfA (2% gesamt)": "11.000,00 EUR"
}

# Anteilige Kosten (10%)
haus_anteilig = [
    ("Grundsteuer (anteilig 10%)", 45.00),
    ("Gebäudeversicherung (anteilig 10%)", 38.00),
    ("Schuldzinsen Kredit (anteilig 10%)", 120.00),
    ("Heizung (Erdgas) (anteilig 10%)", 188.00),
    ("Strom Gesamt (anteilig 10%)", 212.80),
    ("Müll / Abwasser (anteilig 10%)", 65.00),
    ("Reparaturen / Instandhaltung (anteilig 10%)", 120.00),
    ("Gebäude-AfA (anteilig 10%)", 1100.00),
    ("AfA Büromöbel (100% absetzbar)", 833.33)
]

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 16)
        self.cell(0, 10, 'Berechnung der absetzbaren Pauschalen 2025', border=False, align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

pdf = PDF(orientation='P', unit='mm', format='A4')
pdf.add_page()

# Sektion 1: Basisdaten
pdf.set_font('helvetica', 'B', 12)
pdf.set_fill_color(230, 230, 230)
pdf.cell(0, 10, '1. Berechnungsgrundlage', border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
pdf.set_font('helvetica', '', 11)
for k, v in basis.items():
    pdf.cell(60, 8, k + ":", border='L')
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 8, v, border='R', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('helvetica', '', 11)
pdf.ln(5)

# Sektion 2: Anteilige Kosten (10% Werte)
pdf.set_font('helvetica', 'B', 12)
pdf.cell(0, 10, '2. Absetzbare Beträge (bereits auf 10% quotiert)', border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
pdf.set_font('helvetica', 'I', 9)
pdf.multi_cell(0, 5, 'Trage diese Beträge in QuickSteuer ein. Die Umrechnung auf den 10%-Anteil für das Arbeitszimmer wurde hier bereits vorgenommen.')
pdf.ln(2)

pdf.set_font('helvetica', 'B', 10)
pdf.cell(100, 8, 'Kostenart', border=1, fill=True)
pdf.cell(40, 8, 'Absetzbar (10%)', border=1, align='R', fill=True)
pdf.ln()

pdf.set_font('helvetica', '', 11)
total_az = 0
for name, betrag in haus_anteilig:
    pdf.cell(100, 8, name, border=1)
    pdf.cell(40, 8, float_to_german_num(betrag), border=1, align='R')
    pdf.ln()
    total_az += betrag

pdf.set_font('helvetica', 'B', 11)
pdf.cell(100, 10, 'Gesamtsumme Arbeitszimmer', border=1, fill=True)
pdf.cell(40, 10, float_to_german_num(total_az), border=1, align='R', fill=True)
pdf.ln(10)

# Sektion 3: Sonstige Kosten
pdf.set_font('helvetica', 'B', 12)
pdf.cell(0, 10, '3. Sonstige Betriebsausgaben', border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
pdf.set_font('helvetica', '', 11)

# Telefon
pdf.set_font('helvetica', 'B', 11)
pdf.cell(0, 8, 'Telefon & Internet:', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('helvetica', '', 11)
pdf.multi_cell(0, 6, "Basis: 720,00 EUR/Jahr (brutto).\nAbsetzbarer Betrag (50%): 360,00 EUR (brutto).")
pdf.ln(2)

# KFZ
pdf.set_font('helvetica', 'B', 11)
pdf.cell(0, 8, 'Privat-KFZ Fahrten:', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('helvetica', '', 11)
pdf.multi_cell(0, 6, "26 Fahrten à 12 km (einfach) = 624 km Gesamtstrecke.\nEntfernungspauschale: 187,20 EUR.")

pdf.output(pdf_path)
print(f"Bericht auf 10% korrigiert: {pdf_path}")
