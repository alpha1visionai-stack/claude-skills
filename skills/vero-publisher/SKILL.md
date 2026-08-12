---
name: vero-publisher
description: >
  Automatisiertes Veröffentlichen von Fotos mit Bildunterschriften und Hashtags auf Vero (vero.co) über Playwright und Electron CDP.
  Eigenständiger Skill — führt KEINE externen Kamera-/EXIF-Skills aus, sondern publiziert direkt die übergebenen Bilddateien.
  Nutzt die offizielle Vero Desktop-App mit automatischer CDP-Anbindung und persistentem Benutzer-Login.
  Unterstützt Einzel-Uploads, Multi-Foto-Posts (bis zu 9 Bilder), Zielgruppen-Auswahl (Followers/Öffentlich, Freunde, Bekannte, Enge Freunde) und Batch-Warteschlangen (Queue via JSON).
---

# Vero Auto-Publisher Skill

Vollautomatisches Posten von Fotos, Bildunterschriften und Hashtags auf Vero (`vero.co`) über Playwright & Chrome DevTools Protocol (CDP) mit der offiziellen Vero Desktop-App.

> 🔒 **Eigenständig & Isoliert:** Dieser Skill verarbeitet und publiziert ausschließlich die bereitgestellten Bilddateien und triggert keine Filter-, Sensor- oder EXIF-Tools.

## Highlights & Features

* 🚀 **Offizielle Vero Desktop Integration**: Direkte Steuerung der Desktop-App via CDP (`--remote-debugging-port=9222`) – keine inoffiziellen reverse-engineered HTTP-APIs notwendig.
* 🔐 **Persistente Session**: Verwendet automatisch das bestehende Benutzerprofil von Vero (`AppData\Roaming\VERO`). Einmal eingeloggt, bleibt die Sitzung dauerhaft erhalten.
* 🖼️ **Einzel- & Multi-Foto-Support**: Unterstützt das Veröffentlichen einzelner Bilder sowie Galerien/Carousels mit bis zu 9 Bildern pro Beitrag.
* 🎯 **Zielgruppen-/Loop-Auswahl**:
  - `followers` (Standard: Öffentlich / Alle Follower & Verbindungen)
  - `friends` (Freunde & Enge Freunde)
  - `acquaintances` (Bekannte, Freunde & Enge Freunde)
  - `close-friends` (Nur Enge Freunde)
* 📝 **Robuste Text- & Hashtag-Eingabe**: Zuverlässige Tastatureingabe mit automatischer Behandlung von Hashtag-Autocomplete-Popups.
* 📁 **Batch-Upload & Queue**: Mehrere Beiträge aus einer JSON-Warteschlange nacheinander mit einstellbarem Delay posten.
* 🧪 **Dry-Run-Modus**: Testmodus (`--dry-run`), der alle Schritte bis zum finalen Absenden durchläuft und Screenshots zur Vorschau erstellt, ohne den Beitrag zu veröffentlichen.

---

## Installation & Voraussetzungen

1. **Vero Desktop App** muss installiert sein (Standard: `C:\Users\<User>\AppData\Local\Programs\VERO\VERO.exe`).
2. **Playwright & Requests** für Python:
```bash
pip install playwright requests
playwright install chromium
```

---

## Verwendung

### 1. Status & Login prüfen

```bash
python skills/vero-publisher/vero_auth.py
```

### 2. Einzelnes Foto veröffentlichen

```bash
python skills/vero-publisher/vero_post.py \
  --image "D:\Pfad\Zu\Deinem\Bild.jpg" \
  --caption "Street Life in Black and White 📸\n\n#StreetPhotography #BlackAndWhite #Vero" \
  --audience "followers"
```

### 3. Multi-Foto Post (Carousel)

```bash
python skills/vero-publisher/vero_post.py \
  --image "D:\Pfad\Bild1.jpg" "D:\Pfad\Bild2.jpg" "D:\Pfad\Bild3.jpg" \
  --caption "Series: Urban Reflections\n\n#StreetSeries #CityLife"
```

### 4. Caption aus einer Datei laden

```bash
python skills/vero-publisher/vero_post.py \
  --image "D:\Pfad\Zu\Deinem\Bild.jpg" \
  --caption-file "D:\Pfad\caption.txt"
```

### 5. Queue / Batch-Upload

```bash
python skills/vero-publisher/vero_post.py --queue "queue.json" --delay 30
```

*Beispiel `queue.json`:*
```json
[
  {
    "image": "D:\\Bilder\\foto1.jpg",
    "caption": "Erstes Bild auf Vero #photography",
    "audience": "followers"
  },
  {
    "image": ["D:\\Bilder\\foto2.jpg", "D:\\Bilder\\foto3.jpg"],
    "caption": "Zweites Bild (Serie) #street",
    "audience": "friends"
  }
]
```

### 6. Dry-Run (Test ohne Absenden)

```bash
python skills/vero-publisher/vero_post.py \
  --image "D:\Pfad\Zu\Deinem\Bild.jpg" \
  --caption "Test Caption #Testing" \
  --dry-run
```

---

## Parameter

| Argument | Typ | Standard | Beschreibung |
| :--- | :--- | :--- | :--- |
| `--image` | Pfad(e) | `None` | Ein oder mehrere Pfade zu Bilddateien (JPEG, PNG, bis zu 9 Bilder). |
| `--caption` | Text | `""` | Bildunterschrift inklusive Zeilenumbrüchen und `#Hashtags`. |
| `--caption-file` | Pfad | `None` | Pfad zu einer Textdatei mit der Caption. |
| `--audience` | Auswahl | `followers` | Zielgruppe: `followers`, `close-friends`, `friends`, `acquaintances`. |
| `--queue` | Pfad | `None` | JSON-Datei mit einer Liste von Post-Objekten. |
| `--delay` | Sekunden | `30` | Wartezeit in Sekunden zwischen mehreren Beiträgen in der Queue. |
| `--dry-run` | Flag | `False` | Führt alle Schritte bis zur Zielgruppe aus, bricht vor dem Posten ab. |
| `--cdp-port` | Zahl | `9222` | Port für Electron CDP Remote Debugging. |
| `--vero-path` | Pfad | `Auto` | Benutzerdefinierter Pfad zur `VERO.exe`. |
