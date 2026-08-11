import os
import sys
import time
import argparse
import json
import urllib.parse
from playwright.sync_api import sync_playwright

SESSION_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".session")

def log(msg):
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode('ascii', 'replace').decode('ascii'))
    sys.stdout.flush()

def is_user_logged_in(context):
    try:
        cookies = context.cookies("https://www.instagram.com")
        for c in cookies:
            if c.get("name") == "sessionid" and len(c.get("value", "")) > 5:
                return True
    except Exception:
        pass
    return False

def dismiss_popups(page):
    dismiss_selectors = [
        "button:has-text('Not Now')",
        "button:has-text('Jetzt nicht')",
        "button:has-text('Cancel')",
        "button:has-text('Abbrechen')",
        "button:has-text('Allow all cookies')",
        "button:has-text('Alle Cookies erlauben')",
        "button:has-text('Discard')",
        "button:has-text('Verwerfen')"
    ]
    for sel in dismiss_selectors:
        try:
            btn = page.locator(sel)
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click()
                time.sleep(1)
        except Exception:
            pass

def post_to_instagram(image_path, caption, headless=True, aspect="original"):
    if not os.path.exists(SESSION_DIR):
        log(f"Error: Keine Session gefunden in '{SESSION_DIR}'.")
        log("Bitte führe zuerst 'python instagram_auth.py' aus, um dich anzumelden.")
        return False

    abs_image_path = os.path.abspath(image_path)
    if not os.path.exists(abs_image_path):
        log(f"Error: Bilddatei '{abs_image_path}' nicht gefunden.")
        return False

    log(f"\n[Instagram Auto-Post]")
    log(f"Bild: {os.path.basename(abs_image_path)}")
    log(f"Bildpfad: {abs_image_path}")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            headless=headless,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.new_page()

        # Intercept backend media/configure requests to guarantee exact caption injection
        def handle_configure_route(route):
            req = route.request
            post_data = req.post_data or ""
            try:
                params = urllib.parse.parse_qs(post_data)
                params['caption'] = [caption]
                new_post_data = urllib.parse.urlencode(params, doseq=True)
                route.continue_(post_data=new_post_data)
            except Exception:
                route.continue_()

        page.route("**/api/v1/media/configure/**", handle_configure_route)
        page.route("**/api/v1/media/configure/", handle_configure_route)

        try:
            log("-> Öffne Instagram & prüfe Session...")
            page.goto("https://www.instagram.com/", wait_until="networkidle", timeout=45000)
            time.sleep(2)
            dismiss_popups(page)

            if not is_user_logged_in(context):
                log("Error: Kein aktiver Instagram-Login gefunden ('sessionid' fehlt).")
                context.close()
                return False

            log("-> 1. Klicke auf 'Erstellen'...")
            create_link = page.locator("span:has-text('Create'), svg[aria-label='New post'], svg[aria-label='Create']").first
            create_link.click()
            time.sleep(2)

            log("-> 2. Klicke auf 'Post' im Untermenü...")
            post_item = page.get_by_text("Post", exact=True)
            if post_item.count() > 0:
                for idx in range(post_item.count()):
                    if post_item.nth(idx).is_visible():
                        post_item.nth(idx).click()
                        break
            time.sleep(2)

            log("-> 3. Lade Bilddatei hoch...")
            page.locator("input[type='file']").first.set_input_files(abs_image_path)
            time.sleep(3)

            log("-> 4. Weiter zu Filter...")
            page.locator("div[role='dialog']").get_by_text("Next", exact=True).click(force=True)
            time.sleep(2)

            log("-> 5. Weiter zu Bildunterschrift...")
            page.locator("div[role='dialog']").get_by_text("Next", exact=True).click(force=True)
            time.sleep(2)

            log("-> 6. Caption & Tags im Editor eintragen...")
            caption_box = page.locator("div[role='dialog'] div[contenteditable='true'], div[role='dialog'] div[aria-label*='caption' i], div[role='dialog'] div[role='textbox']").first
            if caption_box.count() > 0:
                caption_box.click()
                time.sleep(0.5)
                page.keyboard.type(caption, delay=2)
                time.sleep(1)

            log("-> 7. Veröffentliche Beitrag (Klicke auf 'Share')...")
            share_el = page.locator("div[role='dialog']").get_by_text("Share", exact=True)
            share_el.evaluate("el => el.click()")

            log("-> 8. Warte auf Bestätigung von Instagram...")
            success = False
            for _ in range(35):
                time.sleep(2)
                dialog_text = page.locator("div[role='dialog']").all_text_contents()
                if any("shared" in t.lower() or "geteilt" in t.lower() for t in dialog_text):
                    success = True
                    break
                if page.locator("div[role='dialog'] img[alt*='Animated checkmark']").count() > 0:
                    success = True
                    break

            if success:
                log(">> ERFOLG: Beitrag mit vollständiger Caption & Hashtags erfolgreich geteilt!\n")
            else:
                log(">> Hinweis: Upload-Vorgang abgeschlossen.\n")

            time.sleep(3)
            context.close()
            return True

        except Exception as e:
            log(f">> FEHLER beim Posten: {e}")
            try:
                debug_shot = os.path.join(SESSION_DIR, "error_screenshot.png")
                page.screenshot(path=debug_shot)
                log(f"Debug-Screenshot gespeichert unter: {debug_shot}")
            except Exception:
                pass
            context.close()
            return False

def main():
    parser = argparse.ArgumentParser(description="Instagram Auto-Poster via Playwright")
    parser.add_argument("--image", help="Pfad zum Bild")
    parser.add_argument("--caption", help="Bildunterschrift und Hashtags")
    parser.add_argument("--caption-file", help="Pfad zu einer Textdatei mit der Caption")
    parser.add_argument("--queue", help="JSON-Datei mit mehreren Posts")
    parser.add_argument("--aspect", choices=["original", "1:1", "4:5", "16:9"], default="original", help="Seitenverhältnis")
    parser.add_argument("--headless", action="store_true", default=True, help="Browser im Hintergrund ausführen")
    parser.add_argument("--delay", type=int, default=45, help="Verzögerung in Sekunden zwischen Posts")

    args = parser.parse_args()

    if args.queue:
        with open(args.queue, "r", encoding="utf-8") as f:
            queue_data = json.load(f)
        total = len(queue_data)
        log(f"Starte Queue mit {total} Beiträgen...")
        for idx, item in enumerate(queue_data, start=1):
            img = item.get("image")
            cap = item.get("caption", "")
            asp = item.get("aspect", args.aspect)
            log(f"\n--- Post {idx}/{total} ---")
            success = post_to_instagram(img, cap, headless=args.headless, aspect=asp)
            if idx < total and success:
                log(f"Warte {args.delay} Sekunden bis zum nächsten Post...")
                time.sleep(args.delay)
    elif args.image:
        caption = ""
        if args.caption_file and os.path.exists(args.caption_file):
            with open(args.caption_file, "r", encoding="utf-8") as f:
                caption = f.read()
        elif args.caption:
            caption = args.caption

        post_to_instagram(args.image, caption, headless=args.headless, aspect=args.aspect)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
