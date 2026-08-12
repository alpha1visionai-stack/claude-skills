import os
import sys
import subprocess
import time
import requests
from playwright.sync_api import sync_playwright

DEFAULT_VERO_PATH = os.path.expandvars(r"%LOCALAPPDATA%\Programs\VERO\VERO.exe")
DEFAULT_CDP_PORT = 9222

def log(msg):
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode('ascii', 'replace').decode('ascii'))
    sys.stdout.flush()

def get_vero_path(custom_path=None):
    if custom_path and os.path.exists(custom_path):
        return custom_path
    if os.path.exists(DEFAULT_VERO_PATH):
        return DEFAULT_VERO_PATH
    
    # Check alternate program paths
    alt_path = os.path.expandvars(r"%PROGRAMFILES%\VERO\VERO.exe")
    if os.path.exists(alt_path):
        return alt_path
    return None

def is_cdp_available(port=DEFAULT_CDP_PORT):
    try:
        r = requests.get(f"http://127.0.0.1:{port}/json/version", timeout=1)
        return r.status_code == 200
    except Exception:
        return False

def ensure_vero_running(vero_path=None, port=DEFAULT_CDP_PORT):
    if is_cdp_available(port):
        log(f"[Vero Auth] Vero CDP ist bereits erreichbar auf Port {port}.")
        return True

    exe = get_vero_path(vero_path)
    if not exe:
        log(f"[Vero Auth] FEHLER: VERO.exe konnte nicht gefunden werden.")
        log(f"Gesuchter Pfad: {DEFAULT_VERO_PATH}")
        return False

    log(f"[Vero Auth] Starte Vero mit Remote-Debugging (--remote-debugging-port={port})...")
    subprocess.Popen([exe, f"--remote-debugging-port={port}"])

    for _ in range(25):
        time.sleep(1)
        if is_cdp_available(port):
            log(f"[Vero Auth] Verbindung zu Vero CDP erfolgreich hergestellt.")
            time.sleep(2)
            return True

    log(f"[Vero Auth] FEHLER: Timeout beim Verbindungsaufbau zu Vero CDP.")
    return False

def check_login_status(vero_path=None, port=DEFAULT_CDP_PORT):
    if not ensure_vero_running(vero_path, port):
        return False

    cdp_url = f"http://127.0.0.1:{port}"
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(cdp_url)
            contexts = browser.contexts
            if not contexts or not contexts[0].pages:
                log("[Vero Auth] FEHLER: Keine geöffnete Vero-Seite gefunden.")
                return False

            page = contexts[0].pages[0]
            time.sleep(1)

            # Check if user is logged in (Avatar or Plus button visible)
            avatar_or_plus = page.locator("div.nav-menu-avatar__nav-menu-avatar__kuqfB, div[class*='circle-float-button__base-button'], div.main-stream__container__MCX0O")
            if avatar_or_plus.count() > 0 and avatar_or_plus.first.is_visible():
                log("\n[Vero Auth] Status: EINGELOGGT (Aktiv)")
                log("[Vero Auth] Die Vero Desktop-App ist einsatzbereit für automatische Posts.\n")
                return True
            else:
                log("\n[Vero Auth] Status: NICHT EINGELOGGT")
                log("[Vero Auth] Bitte logge dich einmalig in der geöffneten Vero-App ein.")
                log("[Vero Auth] Nach dem Login bleibt die Sitzung dauerhaft gespeichert.\n")
                return False
        except Exception as e:
            log(f"[Vero Auth] FEHLER bei der Statusprüfung: {e}")
            return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Vero Authentication & Status Check")
    parser.add_argument("--vero-path", default=None, help="Benutzerdefinierter Pfad zu VERO.exe")
    parser.add_argument("--cdp-port", type=int, default=DEFAULT_CDP_PORT, help="CDP Port (Standard: 9222)")
    args = parser.parse_args()

    success = check_login_status(vero_path=args.vero_path, port=args.cdp_port)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
