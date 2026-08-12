import os
import sys
import time
import argparse
import base64
import json
import subprocess
import requests
from playwright.sync_api import sync_playwright

DEFAULT_VERO_PATH = os.path.expandvars(r"%LOCALAPPDATA%\Programs\VERO\VERO.exe")
DEFAULT_CDP_PORT = 9222

AUDIENCE_CHOICES = {
    "followers": "loop_followers",
    "public": "loop_followers",
    "everyone": "loop_followers",
    "friends": "loop_friends",
    "acquaintances": "loop_acquaintances",
    "close-friends": "loop_closefriends",
    "close_friends": "loop_closefriends"
}

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
        return True

    exe = get_vero_path(vero_path)
    if not exe:
        log(f"FEHLER: VERO.exe konnte nicht gefunden werden unter '{DEFAULT_VERO_PATH}'.")
        return False

    log(f"-> Starte Vero Desktop-App (--remote-debugging-port={port})...")
    subprocess.Popen([exe, f"--remote-debugging-port={port}"])

    for _ in range(25):
        time.sleep(1)
        if is_cdp_available(port):
            log("-> Vero CDP bereit.")
            time.sleep(2)
            return True

    log("FEHLER: Konnte keine Verbindung zu Vero CDP herstellen.")
    return False

def reset_open_modals(page):
    """Closes any already open modal or menu before starting a new post."""
    try:
        # Check for bottom floating close button (X)
        close_btn = page.locator("div[class*='circle-float-button__close-button']").first
        if close_btn.is_visible(timeout=500):
            close_btn.click(force=True, timeout=1000)
            time.sleep(1)
    except Exception:
        pass

    try:
        # Check for left header button (Cancel or Back)
        left_btn = page.locator("div.nav-header__buttonLeft__in6BM div").first
        if left_btn.is_visible(timeout=500):
            left_btn.click(force=True, timeout=1000)
            time.sleep(1)
    except Exception:
        pass

def post_to_vero(image_paths, caption="", audience="followers", dry_run=False, vero_path=None, cdp_port=DEFAULT_CDP_PORT):
    """
    Publishes one or more photos with caption and hashtags to Vero (vero.co).
    Independent and self-contained — does NOT trigger any external camera/EXIF skills.
    """
    if isinstance(image_paths, str):
        image_paths = [image_paths]

    # Validate image files
    valid_paths = []
    for p in image_paths:
        abs_p = os.path.abspath(p)
        if not os.path.exists(abs_p):
            log(f"FEHLER: Bilddatei '{abs_p}' existiert nicht.")
            return False
        valid_paths.append(abs_p)

    if not valid_paths:
        log("FEHLER: Keine gültigen Bilddateien übergeben.")
        return False

    if len(valid_paths) > 9:
        log("Warnung: Vero unterstützt maximal 9 Bilder pro Beitrag. Die ersten 9 werden verwendet.")
        valid_paths = valid_paths[:9]

    audience_key = audience.lower().strip()
    loop_target_class = AUDIENCE_CHOICES.get(audience_key, "loop_followers")

    log("\n" + "="*50)
    log("[Vero Auto-Publisher]")
    log(f"Bilder ({len(valid_paths)}): {[os.path.basename(p) for p in valid_paths]}")
    log(f"Zielgruppe: {audience_key} (Icon: {loop_target_class})")
    log(f"Dry-Run (Testmodus): {dry_run}")
    if caption:
        preview_cap = caption.replace('\n', ' ')
        log(f"Caption: {preview_cap[:80]}..." if len(preview_cap) > 80 else f"Caption: {preview_cap}")
    log("="*50)

    if not ensure_vero_running(vero_path, cdp_port):
        return False

    cdp_url = f"http://127.0.0.1:{cdp_port}"
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(cdp_url)
            if not browser.contexts or not browser.contexts[0].pages:
                log("FEHLER: Keine geöffnete Vero-Seite gefunden.")
                return False

            page = browser.contexts[0].pages[0]
            time.sleep(1)

            # 1. Reset any open dialogs
            reset_open_modals(page)

            # 2. Open "+" menu
            log("-> 1. Öffne Beitrags-Menü (+)...")
            plus_btn = page.locator("div[class*='circle-float-button__base-button']").first
            if not plus_btn.is_visible(timeout=3000):
                log("FEHLER: Plus-Button nicht gefunden. Ist Vero eingeloggt?")
                return False
            plus_btn.click(force=True, timeout=3000)
            time.sleep(1)

            # 3. Click "PHOTO"
            log("-> 2. Wähle 'PHOTO'...")
            photo_link = page.locator("div.create-post__button-group__uhCCc a").first
            if not photo_link.is_visible(timeout=3000):
                log("FEHLER: 'PHOTO' Menüpunkt nicht sichtbar.")
                return False
            photo_link.click(force=True, timeout=3000)
            time.sleep(1.5)

            # 4. Inject image files via dropzone
            log(f"-> 3. Lade {len(valid_paths)} Bild(er) in den Vero Drop-Bereich hoch...")
            images_data = []
            for pth in valid_paths:
                with open(pth, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode("ascii")
                images_data.append({"name": os.path.basename(pth), "b64": b64})

            drop_res = page.evaluate("""(images) => {
                const dropEl = document.querySelector("div[class*='add-photo__drop-region']");
                if (!dropEl) return {error: "Drop element not found"};

                const dt = new DataTransfer();
                const files = [];

                for (let img of images) {
                    const byteCharacters = atob(img.b64);
                    const byteNumbers = new Array(byteCharacters.length);
                    for (let i = 0; i < byteCharacters.length; i++) {
                        byteNumbers[i] = byteCharacters.charCodeAt(i);
                    }
                    const byteArray = new Uint8Array(byteNumbers);
                    const blob = new Blob([byteArray], {type: 'image/jpeg'});
                    const file = new File([blob], img.name, {type: 'image/jpeg', lastModified: Date.now()});
                    dt.items.add(file);
                    files.push(file);
                }

                const dropEvt = new DragEvent('drop', {
                    bubbles: true,
                    cancelable: true,
                    dataTransfer: dt
                });

                Object.defineProperty(dropEvt, 'dataTransfer', {
                    value: {
                        files: files,
                        items: files,
                        types: ['Files']
                    }
                });

                dropEl.dispatchEvent(dropEvt);
                return { success: true, count: files.length };
            }""", images_data)

            if not drop_res.get("success"):
                log(f"FEHLER beim Bild-Upload: {drop_res}")
                return False

            time.sleep(2.5)

            # 5. Click "Next" on Photo screen
            log("-> 4. Bestätige Bildauswahl (Weiter)...")
            next_btn = page.locator("div.nav-header__buttonRight__iqSgO div:not([class*='disabled'])").first
            next_btn.click(force=True, timeout=4000)
            time.sleep(1.5)

            # 6. Type Caption & Tags
            if caption:
                log("-> 5. Trage Bildunterschrift & Hashtags ein...")
                editable_box = page.locator("div.segments-textarea__generated__vZhUO, div.segments-textarea__segments-textarea__Eqamk").first
                if editable_box.is_visible(timeout=3000):
                    editable_box.click(force=True, timeout=2000)
                    time.sleep(0.3)
                    page.keyboard.type(caption, delay=5)
                    time.sleep(0.5)
                    # Dismiss autocomplete overlay if present
                    page.keyboard.press("Escape")
                    time.sleep(0.3)
            else:
                log("-> 5. Keine Bildunterschrift übergeben (überspringe)...")

            # 7. Click "Next" to go to Audience selection
            log("-> 6. Weiter zur Zielgruppen-Auswahl...")
            next_btn2 = page.locator("div.nav-header__buttonRight__iqSgO div:not([class*='disabled'])").first
            next_btn2.click(force=True, timeout=4000)
            time.sleep(1.5)

            # 8. Select Audience loop
            log(f"-> 7. Setze Zielgruppe auf '{audience_key}'...")
            loop_icon = page.locator(f"div[class*='{loop_target_class}']").first
            if loop_icon.is_visible(timeout=2000):
                loop_icon.click(force=True, timeout=2000)
                time.sleep(0.8)
            else:
                log(f"Hinweis: Zielgruppen-Icon '{loop_target_class}' nicht direkt gefunden, behalte Standard bei.")

            # 9. Dry Run or Final Post
            if dry_run:
                log("-> [DRY-RUN] Testmodus aktiv: Post wird NICHT abgesendet.")
                screenshot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dry_run_preview.png")
                page.screenshot(path=screenshot_path)
                log(f"-> [DRY-RUN] Vorschau-Screenshot gespeichert unter: {screenshot_path}")
                reset_open_modals(page)
                log("[Vero Auto-Publisher] Dry-Run erfolgreich abgeschlossen! ✓\n")
                return True

            log("-> 8. Veröffentliche Beitrag auf Vero...")
            post_btn = page.locator("div.nav-header__buttonRight__iqSgO div:not([class*='disabled'])").first
            post_btn.click(force=True, timeout=4000)

            # Wait for modal to close (confirming post success)
            log("-> 9. Warte auf Bestätigung...")
            for _ in range(20):
                time.sleep(1)
                modal_present = page.locator("div.modal-body-v2__modal-body-v2__gyfSX").is_visible(timeout=500)
                if not modal_present:
                    log("\n[Vero Auto-Publisher] Beitrag ERFOLGREICH auf Vero veröffentlicht! ✓\n")
                    return True

            log("\n[Vero Auto-Publisher] Hinweis: Post-Dialog wurde gesendet.\n")
            return True

        except Exception as e:
            log(f"FEHLER beim Ausführen des Vero-Publishers: {e}")
            return False

def run_queue(queue_file, delay=30, dry_run=False, vero_path=None, cdp_port=DEFAULT_CDP_PORT):
    if not os.path.exists(queue_file):
        log(f"FEHLER: Queue-Datei '{queue_file}' nicht gefunden.")
        return False

    with open(queue_file, "r", encoding="utf-8") as f:
        queue_data = json.load(f)

    if not isinstance(queue_data, list):
        log("FEHLER: Queue-Datei muss eine JSON-Liste von Post-Objekten enthalten.")
        return False

    total = len(queue_data)
    log(f"\nStarte Batch-Queue mit {total} Beiträgen (Delay: {delay}s)...")

    for i, item in enumerate(queue_data, 1):
        log(f"\n--- Post {i}/{total} ---")
        images = item.get("image") or item.get("images")
        caption = item.get("caption", "")
        audience = item.get("audience", "followers")

        success = post_to_vero(
            image_paths=images,
            caption=caption,
            audience=audience,
            dry_run=dry_run,
            vero_path=vero_path,
            cdp_port=cdp_port
        )

        if not success:
            log(f"Warnung: Fehler bei Post {i}/{total}.")

        if i < total and delay > 0:
            log(f"Warte {delay} Sekunden bis zum nächsten Beitrag...")
            time.sleep(delay)

    log("\n[Vero Auto-Publisher] Warteschlange komplett abgearbeitet! ✓\n")
    return True

def main():
    parser = argparse.ArgumentParser(description="Vero Auto-Publisher Skill")
    parser.add_argument("--image", nargs="+", help="Ein oder mehrere Pfade zu Bilddateien (bis zu 9 Bilder)")
    parser.add_argument("--caption", default="", help="Bildunterschrift mit Text und Hashtags")
    parser.add_argument("--caption-file", default=None, help="Pfad zu einer Textdatei mit der Bildunterschrift")
    parser.add_argument("--audience", default="followers", choices=["followers", "public", "friends", "acquaintances", "close-friends"], help="Zielgruppe")
    parser.add_argument("--queue", default=None, help="Pfad zu einer JSON-Warteschlangen-Datei")
    parser.add_argument("--delay", type=int, default=30, help="Verzögerung in Sekunden zwischen Queue-Posts")
    parser.add_argument("--dry-run", action="store_true", help="Testlauf ohne tatsächliches Absenden")
    parser.add_argument("--vero-path", default=None, help="Benutzerdefinierter Pfad zu VERO.exe")
    parser.add_argument("--cdp-port", type=int, default=DEFAULT_CDP_PORT, help="CDP Port (Standard: 9222)")

    args = parser.parse_args()

    caption_text = args.caption
    if args.caption_file:
        if os.path.exists(args.caption_file):
            with open(args.caption_file, "r", encoding="utf-8") as f:
                caption_text = f.read().strip()
        else:
            log(f"FEHLER: Caption-Datei '{args.caption_file}' nicht gefunden.")
            sys.exit(1)

    if args.queue:
        success = run_queue(
            queue_file=args.queue,
            delay=args.delay,
            dry_run=args.dry_run,
            vero_path=args.vero_path,
            cdp_port=args.cdp_port
        )
    elif args.image:
        success = post_to_vero(
            image_paths=args.image,
            caption=caption_text,
            audience=args.audience,
            dry_run=args.dry_run,
            vero_path=args.vero_path,
            cdp_port=args.cdp_port
        )
    else:
        parser.print_help()
        sys.exit(1)

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
