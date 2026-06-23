# -*- coding: utf-8 -*-
import pandas as pd
import os

# --- KONFIGURATION DER TATSÄCHLICHEN KOSTEN (WOHNEIGENTUM 2025) ---

FLAECHE_GESAMT = 150.0        
FLAECHE_ARBEITSZIMMER = 15.0  

GEBAEUDE_ANSCHAFFUNGSKOSTEN = 550000.0  
AFA_SATZ = 0.02                        

HAUS_KOSTEN_JAHR = {
    "Grundsteuer": 450.0,
    "Gebaeudeversicherung": 380.0,
    "Schuldzinsen_Kredit": 1200.0, # 3% von 40.000 EUR Restschuld
    "Heizung_Erdgas": 1880.0,      
    "Strom_Gesamt": 2128.0,        
    "Muell_Abwasser": 650.0,
    "Reparaturen_Instandhaltung": 1200.0 
}

# Weitere Pauschalen 2025
TELEFON_MONAT_BRUTTO = 60.0
BETRIEBLICHER_ANTEIL_TEL = 0.50 
KM_PRO_STRECKE_EINFACH = 12.0 
FAHRTEN_PRO_JAHR = 26 

# --- KONFIGURATION DIENSTREISE USA (DEZ 2025 - DEFENSIV) ---
VMA_USA_LA_VOLL = 58.00         
VMA_USA_LA_AN_AB = 39.00        

USA_REISE_BUSINESS_TAGE = 2     # Nur Meeting-Tage (Defensiv)
FLUG_TICKET_BETRAG = 950.00     # Dein separates Ticket

# Mietwagen/Tanken im defensiven Modus bewusst auf 0.0
MIETWAGEN_RECHNUNG_NETTO = 0.0
TANKKOSTEN_SCHAETZUNG_USA = 0.0

def calculate_tax_data():
    results = []
    anteil = FLAECHE_ARBEITSZIMMER / FLAECHE_GESAMT
    
    # 1. Arbeitszimmer
    jahres_afa = GEBAEUDE_ANSCHAFFUNGSKOSTEN * AFA_SATZ
    az_afa = jahres_afa * anteil
    
    for name, betrag in HAUS_KOSTEN_JAHR.items():
        betrieblicher_betrag = betrag * anteil
        mwst_anteil = 0.0
        if name in ["Strom_Gesamt", "Heizung_Erdgas", "Reparaturen_Instandhaltung"]:
            netto = betrieblicher_betrag / 1.19
            mwst_anteil = betrieblicher_betrag - netto
            betrieblicher_betrag = netto

        results.append({
            "datum": "2025-12-31",
            "aussteller": f"Hauskosten: {name}",
            "betrag_netto": round(betrieblicher_betrag, 2),
            "mwst": round(mwst_anteil, 2),
            "kategorie": "Freiberuflich_Ausgabe",
            "begruendung": "Anteiliges Arbeitszimmer"
        })

    results.append({
        "datum": "2025-12-31", "aussteller": "Gebäude-AfA", "betrag_netto": round(az_afa, 2),
        "mwst": 0.0, "kategorie": "Freiberuflich_Ausgabe", "begruendung": "Abschreibung AZ"
    })
    
    # 2. Telefon & KFZ Inland
    tel_brutto_jahr = TELEFON_MONAT_BRUTTO * 12 * BETRIEBLICHER_ANTEIL_TEL
    tel_netto = tel_brutto_jahr / 1.19
    results.append({
        "datum": "2025-12-31", "aussteller": "Telefon", "betrag_netto": round(tel_netto, 2),
        "mwst": round(tel_brutto_jahr - tel_netto, 2), "kategorie": "Freiberuflich_Ausgabe", "begruendung": "Telefonanteil"
    })
    
    kfz_kosten = KM_PRO_STRECKE_EINFACH * 2 * FAHRTEN_PRO_JAHR * 0.30
    results.append({
        "datum": "2025-12-31", "aussteller": "Privat-KFZ", "betrag_netto": round(kfz_kosten, 2),
        "mwst": 0.0, "kategorie": "Freiberuflich_Ausgabe", "begruendung": "Fahrten Kronberg-Bad Homburg"
    })

    # 3. Abschreibung Büromöbel (Einbauschränke & Schreibtisch)
    # Basis 10.000 EUR, 12 Jahre Nutzungsdauer (laut QuickSteuer)
    results.append({
        "datum": "2025-12-31", "aussteller": "AfA Büromöbel", "betrag_netto": 833.33,
        "mwst": 0.0, "kategorie": "Freiberuflich_Ausgabe", "begruendung": "Einbauschränke & Schreibtisch (100% AZ)"
    })

    # 4. DIENSTREISE USA (NICHT BERÜCKSICHTIGT)
    # VMA und Flugkosten wurden auf Wunsch entfernt.

    return results

def main():
    output_file = "steuer_erfassung.csv"
    new_data = calculate_tax_data()
    df_new = pd.DataFrame(new_data)
    if os.path.exists(output_file):
        df_old = pd.read_csv(output_file)
        df_old = df_old[df_old['datum'] != "2025-12-31"]
        df_final = pd.concat([df_old, df_new], ignore_index=True, sort=False)
    else: df_final = df_new
    df_final.to_csv(output_file, index=False, encoding='utf-8-sig')
    print("CSV mit defensiven USA-Daten aktualisiert.")

if __name__ == "__main__":
    main()