import os
import sys
import time
from playwright.sync_api import sync_playwright

SESSION_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".session")

def is_user_logged_in(context):
    """Checks if the Instagram sessionid cookie is present and valid."""
    try:
        cookies = context.cookies("https://www.instagram.com")
        for c in cookies:
            if c.get("name") == "sessionid" and len(c.get("value", "")) > 5:
                return True
    except Exception:
        pass
    return False

def run_login():
    os.makedirs(SESSION_DIR, exist_ok=True)
    print("=" * 65)
    print("=== Instagram Playwright Authentifizierung ===")
    print(f"Session-Verzeichnis: {SESSION_DIR}")
    print("=" * 65)
    print("Ein Chrome-Fenster wird geöffnet.")
    print("Bitte logge dich mit deinen Zugangsdaten bei Instagram ein...")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=False,
            viewport={"width": 1280, "height": 900},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )
        page = context.new_page()
        
        # Navigate directly to Instagram Login
        page.goto("https://www.instagram.com/accounts/login/", wait_until="domcontentloaded")
        time.sleep(2)

        # Accept cookie banner if present
        try:
            cookie_buttons = page.locator("button:has-text('Allow all cookies'), button:has-text('Alle Cookies erlauben'), button:has-text('Erforderliche und optionale Cookies erlauben'), button:has-text('Nur erforderliche Cookies erlauben')")
            if cookie_buttons.count() > 0:
                cookie_buttons.first.click()
                time.sleep(1)
        except Exception:
            pass

        print("\n" + "#" * 60)
        print("SCHRITTE IM BROWSER:")
        print("1. Gib Benutzername und Passwort ein und klicke auf 'Anmelden'.")
        print("2. Führe 2FA durch (falls aktiv).")
        print("3. Bestätige 'Informationen speichern'.")
        print("4. Das Skript erkennt den Login automatisch über den Session-Token!")
        print("#" * 60 + "\n")

        max_wait_seconds = 300
        start_time = time.time()
        logged_in = False

        while time.time() - start_time < max_wait_seconds:
            if is_user_logged_in(context):
                logged_in = True
                break
            time.sleep(2)

        if logged_in:
            print("\n>> [ERFOLG] 'sessionid'-Cookie erfolgreich erkannt!")
            print(">> Instagram-Sitzung ist aktiv und gespeichert.")
            time.sleep(3)
        else:
            print("\n>> [TIMEOUT] Keine erfolgreiche Anmeldung innerhalb von 5 Minuten erkannt.")

        context.close()

if __name__ == "__main__":
    run_login()
