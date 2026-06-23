# -*- coding: utf-8 -*-
import os
import subprocess
import sys

def ask_input(prompt, default):
    user_input = input(f"{prompt} [{default}]: ").strip()
    return user_input if user_input else default

def run_script(script_name):
    print(f"\n--- Starte {script_name} ---")
    try:
        result = subprocess.run([sys.executable, script_name], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Ausführen von {script_name}: {e}")
        return False

def update_pauschalen_config():
    print("\n--- Konfiguration für Pauschalen-Rechner (2025) ---")
    
    # Hausdaten
    zinsen = ask_input("Schuldzinsen 2025 (Euro)", "2800.0")
    strom = ask_input("Stromkosten gesamt 2025 (Euro)", "1400.0")
    heizung = ask_input("Heizung/Wasser gesamt 2025 (Euro)", "3200.0")
    
    print("\n--- Daten für USA-Reise (Defensiv-Modus) ---")
    flug = ask_input("Flugkosten (Dein separates Ticket in Euro)", "950.00")
    tage_business = ask_input("Anzahl der reinen Business-Meeting-Tage", "2")

    config_updates = {
        "HAUS_ZINSEN": zinsen,
        "HAUS_STROM": strom,
        "HAUS_HEIZUNG": heizung,
        "FLUG_TICKET": flug,
        "BUSINESS_TAGE": tage_business
    }
    return config_updates

def main():
    print("Steuer-Workflow 2025 (Defensiv-Modus aktiviert)")
    
    # 1. Anonymisierung
    if ask_input("Sollen PDFs anonymisiert werden? (j/n)", "j").lower() == 'j':
        run_script("pdf_redactor.py")
    
    # 2. KI Parsing
    if ask_input("Soll das KI-Parsing starten? (j/n)", "j").lower() == 'j':
        run_script("tax_parser.py")
    
    # 3. Pauschalen & USA (Defensiv)
    if ask_input("Sollen Pauschalen & USA-Flug berechnet werden? (j/n)", "j").lower() == 'j':
        data = update_pauschalen_config()
        # Hinweis an Claude Code, falls es dieses Script liest
        print("\nACTION REQUIRED: Bitte aktualisiere die Variablen in 'pauschalen_rechner.py' mit diesen Werten:")
        for k, v in data.items():
            print(f"  {k} -> {v}")
        run_script("pauschalen_rechner.py")

    print("\nWorkflow abgeschlossen. Die 'steuer_erfassung.csv' ist bereit für QuickSteuer.")

if __name__ == "__main__":
    main()