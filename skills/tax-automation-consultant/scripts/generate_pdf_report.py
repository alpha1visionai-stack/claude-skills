import pandas as pd
from fpdf import FPDF
import os

# Pfade
csv_path = r'D:\OneDrive\Dokumente\KI-Beratung\2025\belege_anonym Ausgaben\Ausgabenübersicht_2025.csv'
pdf_path = r'D:\OneDrive\Dokumente\KI-Beratung\2025\Berichte\Ausgabenbericht_2025.pdf'

def german_num_to_float(val):
    if pd.isna(val) or val == '':
        return 0.0
    val_str = str(val).replace('.', '').replace(',', '.')
    try:
        return float(val_str)
    except:
        return 0.0

def float_to_german_num(val):
    return f"{val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# CSV laden
df = pd.read_csv(csv_path, sep=';', encoding='utf-8')

# Daten konvertieren
df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y')
df['Nettobetrag'] = df['Nettobetrag'].apply(german_num_to_float)
df['MwSt'] = df['MwSt'].apply(german_num_to_float)
df['Bruttobetrag'] = df['Bruttobetrag'].apply(german_num_to_float)

# Sortieren
df = df.sort_values(by=['Kategorie', 'Datum'])

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 16)
        if self.page_no() > 0: # Header auf jeder Seite
             self.cell(0, 10, 'Ausgabenbericht 2025', border=False, align='C', new_x="LMARGIN", new_y="NEXT")
             self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Seite {self.page_no()}/{{nb}}', align='C')

pdf = PDF(orientation='L', unit='mm', format='A4')
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font('helvetica', '', 10)

cols = [
    ('Datum', 25),
    ('Kategorie', 50),
    ('Beschreibung', 110),
    ('Netto', 25),
    ('MwSt', 25),
    ('Brutto', 25)
]

def print_table_header():
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    for col_name, width in cols:
        pdf.cell(width, 8, col_name, border=1, align='C', fill=True)
    pdf.ln()
    pdf.set_font('helvetica', '', 10)

grand_netto = 0
grand_mwst = 0
grand_brutto = 0

categories = sorted(df['Kategorie'].unique())

for cat in categories:
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, f'Kategorie: {cat}', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    print_table_header()
    
    cat_df = df[df['Kategorie'] == cat]
    cat_netto = 0
    cat_mwst = 0
    cat_brutto = 0
    
    for _, row in cat_df.iterrows():
        datum_str = row['Datum'].strftime('%d.%m.%Y')
        pdf.cell(25, 7, datum_str, border=1)
        pdf.cell(50, 7, str(row['Kategorie'])[:25], border=1)
        
        desc = str(row['Text der Ausgabe'])
        if len(desc) > 60:
            desc = desc[:57] + "..."
        pdf.cell(110, 7, desc, border=1)
        
        pdf.cell(25, 7, float_to_german_num(row['Nettobetrag']), border=1, align='R')
        pdf.cell(25, 7, float_to_german_num(row['MwSt']), border=1, align='R')
        pdf.cell(25, 7, float_to_german_num(row['Bruttobetrag']), border=1, align='R')
        pdf.ln()
        
        cat_netto += row['Nettobetrag']
        cat_mwst += row['MwSt']
        cat_brutto += row['Bruttobetrag']
        
    # Summe für Kategorie
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(25 + 50 + 110, 8, f'Summe {cat}', border=1, align='R')
    pdf.cell(25, 8, float_to_german_num(cat_netto), border=1, align='R')
    pdf.cell(25, 8, float_to_german_num(cat_mwst), border=1, align='R')
    pdf.cell(25, 8, float_to_german_num(cat_brutto), border=1, align='R')
    pdf.ln()
    
    grand_netto += cat_netto
    grand_mwst += cat_mwst
    grand_brutto += cat_brutto

# Gesamtsumme auf letzter Seite
pdf.add_page()
pdf.set_font('helvetica', 'B', 16)
pdf.cell(0, 20, 'GESAMTAUFSTELLUNG 2025', new_x="LMARGIN", new_y="NEXT", align='C')
pdf.ln(10)

pdf.set_font('helvetica', 'B', 12)
pdf.set_fill_color(220, 220, 220)
pdf.cell(100, 10, 'Posten', border=1, fill=True)
pdf.cell(40, 10, 'Betrag', border=1, align='R', fill=True)
pdf.ln()

pdf.set_font('helvetica', '', 12)
pdf.cell(100, 10, 'Gesamtsumme Netto', border=1)
pdf.cell(40, 10, float_to_german_num(grand_netto), border=1, align='R')
pdf.ln()
pdf.cell(100, 10, 'Gesamtsumme MwSt', border=1)
pdf.cell(40, 10, float_to_german_num(grand_mwst), border=1, align='R')
pdf.ln()
pdf.set_font('helvetica', 'B', 12)
pdf.cell(100, 10, 'Gesamtsumme Brutto', border=1, fill=True)
pdf.cell(40, 10, float_to_german_num(grand_brutto), border=1, align='R', fill=True)

pdf.output(pdf_path)
print(f"Bericht mit Seitenumbrüchen erfolgreich unter {pdf_path} gespeichert.")
