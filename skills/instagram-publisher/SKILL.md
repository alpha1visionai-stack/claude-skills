---
name: instagram-publisher
description: >
  Automatisiertes Veröffentlichen von Bildern mit Bildunterschriften und Hashtags auf Instagram über Playwright in ihren Original-Dimensionen (Aspect Ratio: Original).
  Eigenständiger Skill — führt KEINE externen Kamera-/EXIF-Skills aus, sondern publiziert direkt die übergebenen Bilddateien.
  Verwendet eine persistent gespeicherte Browser-Sitzung (.session), um Logins und 2FA zu speichern.
  Unterstützt Einzel-Uploads, Warteschlangen (Queue via JSON), Seitenverhältnis-Anpassungen (original, 1:1, 4:5, 16:9),
  und manipulationssichere Backend-Caption-Injektion für fehlerfreie Veröffentlichung ohne Textverlust.
---

# Instagram Auto-Publisher Skill

Vollautomatisches Posten von Fotos in **Original-Dimensionen**, Bildunterschriften und Hashtags auf Instagram über Playwright Chromium mit persistentem Login.

> 🔒 **Eigenständig & Isoliert:** Dieser Skill verarbeitet und publiziert ausschließlich die bereitgestellten Bilddateien und triggert keine Filter-, Sensor- oder EXIF-Tools.

## Highlights & Features

* 📐 **Original-Dimensionen (Standard: `original`)**: Wählt im Upload-Dialog automatisch „Original“ aus, um quadratischen 1:1-Beschnitt zu verhindern.
* 🔐 **Persistente Session (.session)**: Einmaliges Login im sichtbaren Browser (inkl. 2FA), Session bleibt dauerhaft für alle zukünftigen Uploads gespeichert.
* 🚀 **Robuste API-Injektion**: Umgeht Web-Editor-Bugs (z. B. Metas Lexical/React-State) durch direkte, sichere Injektion der Caption & Hashtags in die Backend-Anfrage (`/api/v1/media/configure/`).
* 📁 **Batch-Upload & Queue**: Mehrere Beiträge mit zeitlicher Verzögerung (Delay) nacheinander veröffentlichen.
* 🤖 **Headless-Modus**: Läuft standardmäßig geräuschlos im Hintergrund.

---

## Installation & Voraussetzungen

```bash
pip install playwright
playwright install chromium
```

---

## Verwendung

### 1. Einmalige Anmeldung (Initialisierung der Session)

```bash
python skills/instagram-publisher/instagram_auth.py
```

### 2. Einzelnes Bild im Original-Format posten

```bash
python skills/instagram-publisher/instagram_post.py \
  --image "D:\Pfad\Zu\Deinem\Bild.jpg" \
  --aspect "original" \
  --caption "Titel oder Bildbeschreibung.\n\n#StreetPhotography #BlackAndWhite"
```

### 3. Queue (mehrere Bilder als Batch in Original-Dimensionen)

```bash
python skills/instagram-publisher/instagram_post.py --queue "queue.json" --delay 45
```

---

## Parameter

| Argument | Typ | Standard | Beschreibung |
| :--- | :--- | :--- | :--- |
| `--image` | Pfad | `None` | Pfad zur Bilddatei (JPEG, PNG). |
| `--caption` | Text | `""` | Bildunterschrift inklusive Zeilenumbrüchen und `#Hashtags`. |
| `--caption-file`| Pfad | `None` | Pfad zu einer Textdatei mit der Caption. |
| `--queue` | Pfad | `None` | JSON-Datei mit einer Liste von Post-Objekten. |
| `--aspect` | Auswahl | `original` | Seitenverhältnis (`original`, `1:1`, `4:5`, `16:9`). Standard: `original`. |
| `--delay` | Sekunden | `45` | Wartezeit in Sekunden zwischen mehreren Posts in der Queue. |
| `--headless` | Flag | `True` | Browser im Hintergrund ausführen (Standard: True). |
