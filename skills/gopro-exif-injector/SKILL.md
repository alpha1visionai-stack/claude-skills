---
name: gopro-exif-injector
description: >
  Injiziert realistische GoPro EXIF-Metadaten (HERO11/HERO12 Black, 2.7mm f/2.5 Linse, 15mm 35mm-Äquivalent), simuliert physikalische Kamera- & Sensor-Charakteristiken (Chromatische Aberration, S-Gradationskurve, RAW/CMOS-Sensorrauschen) und wendet DxO Nik 7 Color Efex Filter ("Ai-gen-2": Monday Morning Glow, Dual Film Grain, optional Darken/Lighten Center Vignette) sowie optional eine zusätzliche S/W-Version mit DxO Silver Efex Pro ("019 - Fine Art Process") an.
  Erzeugt automatisch versionierte Ausgabedateien (_v1, _v2, etc.) zum Schutz der Originale.
  Berücksichtigt automatisch oder manuell Tag- und Nachtszenen (ISO 100-3200, Verschlusszeit 1/30 bis 1/2000s, Program AE, GoPro Firmware).
  Verwenden, wenn der Benutzer sagt: "Füge GoPro EXIF Daten ein", "Schreibe realistische Metadaten in die Bilder", "GoPro Exif injecten", "Wende Nik 7 Color Efex Ai-gen-2 an", "Erstelle eine S/W Fine Art Version mit Silver Efex 019", "Chromatische Aberration und Rauschen hinzufügen" oder ähnliches.
---

# GoPro EXIF, Sensor Realism & DxO Nik 7 Color Efex / Silver Efex Skill

Dieses Tool kombiniert technisch akkurate GoPro EXIF-Metadaten mit physikalischer Sensor- und Optik-Simulation, dem **DxO Nik 7 Color Efex Preset `AI-gen-2`** und einer High-End S/W-Fine-Art-Konvertierung nach **DxO Silver Efex Pro `019 - Fine Art Process`**, um KI-generierten Bildern die charakteristische Signatur echter Aufnahmen zu verleihen.

> 💾 **Auto-Versionierung:** Jeder Durchlauf erzeugt standardmäßig eine neue versionierte Datei (`dateiname_v1.jpg`, `dateiname_v2.jpg` etc.). Das Original bleibt unverändert.

---

## Enthaltene Bildverarbeitungs- & Filter-Pipeline

1. **DxO Nik 7 Color Efex `Ai-gen-2` Filterkette (Farbe)**:
   - **Monday Morning**: *Verschmieren auf 0* (volle Detailschärfe ohne künstliche Weichzeichnung/Diffusion), *Farbe erhöht* (+25% Farbsättigung für lebendige Farben) und feiner Helligkeitslift.
   - **Dual-Layer Film Grain**: Kombination aus weichem Korn und hochfrequentem Mikro-Korn mit Schatten- & Spitzlichterschutz.
   - **Darken / Lighten Center (optional, Standard: aus)**: Subtile Mitten-Aufhellung (+25%) bei fließender Rand-Vignettierung (kann via `--center-vignette` aktiviert und via `--vignette-strength <wert>` skaliert werden).

2. **DxO Silver Efex Pro `019 - Fine Art Process` (Zusätzliche S/W-Version)**:
   - **Neutrale Monochrom-Tonung**: Präzise Luminanz-Balance ohne Farbstiche.
   - **Global Contrast (+18.6%) & Soft Contrast (-31.7%)**: Sattes Tiefenschwarz bei gleichzeitig seidenweichen Mitteltönen und geschützten Highlights.
   - **Multi-Scale Structure**: *Fine Structure (+44.5%)* für gestochen scharfe Mikrodetails (Haare, Texturen, Kanten) kombiniert mit *Med Structure (-17.1%)* für samtige, edle Haut- und Flächenübergänge.
   - **Silver Halide Film Grain (500)**: Echtes organisches Silberhalogenid-Filmkorn mit Lichterschutz.

3. **Optische Sensor-Simulation**:
   - **Chromatische Aberration (Transversale CA / TCA)**: Radiale Farbverschiebungen (Rot outward / Blau inward), die zu den Bildrändern hin zunehmen (typisch für 15mm Superweitwinkel).
   - **Sensor-Gradationskurve (S-Curve)**: Schwarzwert-Lift (kein 0-Clipping) + weicher Highlight Roll-off (kein 255-Abriss).
   - **CMOS-Sensorrauschen**: Echtes, intensitätsgewichtetes Photonenrauschen in dunklen Bereichen.

4. **GoPro EXIF-Metadaten**:
   - Vollständiges EXIF-Profil für Farb- und S/W-Dateien (HERO12 Black / HERO11 Black, 2.7mm f/2.5, 15mm Äquivalent, ISO 100-3200, Program AE, Firmware v2.20).

---

## Technische EXIF-Spezifikationen

| Parameter | Nachtaufnahme (Low Light / Nightlife) | Tagesaufnahme (Sonnig) | Tagesaufnahme (Bewölkt) |
| :--- | :--- | :--- | :--- |
| **Make** | `GoPro` | `GoPro` | `GoPro` |
| **Model** | `HERO12 Black` (oder `HERO11 Black`) | `HERO12 Black` | `HERO12 Black` |
| **Focal Length** | `2.7 mm` (physikalisch) | `2.7 mm` | `2.7 mm` |
| **35mm Equivalent** | `15 mm` (Super-Weitwinkel) | `15 mm` | `15 mm` |
| **F-Number** | `f/2.5` (Festblende) | `f/2.5` | `f/2.5` |
| **ISO-Speed** | `1600` bis `3200` | `100` | `250` bis `400` |
| **ExposureTime** | `1/30` bis `1/50` sec | `1/1000` bis `1/2000` sec | `1/250` bis `1/500` sec |
| **ExposureProgram** | `Program AE` | `Program AE` | `Program AE` |
| **Software** | `GoPro Firmware v2.20` | `GoPro Firmware v2.20` | `GoPro Firmware v2.20` |
| **SceneCaptureType**| `Night` | `Standard` | `Standard` |

---

## Auslöser in natürlicher Sprache (Trigger Phrases)

- *"Wende DxO Nik 7 Color Efex mit dem Filter Ai-gen-2 auf die Bilder an und erstelle zusätzlich eine S/W-Version nach Silver Efex 019 Fine Art."*
- *"Erstelle von jedem Bild eine Farb- und eine S/W Fine-Art-Version mit GoPro EXIF Daten."*
- *"Füge realistische GoPro EXIF-Daten, Sensor-Rauschen und Nik Color/Silver Efex Effekte ein."*
- *"Wende den GoPro-Skill mit S/W Fine Art Filter an."*

---

## CLI-Befehle

### 1. Farb- und zusätzliche S/W-Version (Silver Efex 019 Fine Art) erstellen:
```bash
python skills/gopro-exif-injector/inject_gopro_exif.py "<PFAD_ZUM_ORDNER_ODER_BILD>" --bw
```
*Erzeugt für jedes Bild zwei versionierte Ausgabedateien: `bild_v1.jpg` (Farbe) und `bild_v1_NIK.jpg` (S/W Fine Art).*

### 2. Nur die S/W Fine-Art Version erstellen:
```bash
python skills/gopro-exif-injector/inject_gopro_exif.py "<PFAD>" --bw-only
```

### 3. Standard-Farbbearbeitung (Erzeugt automatisch `_v1.jpg`, `_v2.jpg` etc.):
```bash
python skills/gopro-exif-injector/inject_gopro_exif.py "<PFAD>"
```

### 4. Mit Center-Boost & Rand-Vignettierung:
```bash
python skills/gopro-exif-injector/inject_gopro_exif.py "<PFAD>" --center-vignette
```

### 5. Ohne Versionierung (Überschreibt Originaldatei direkt in-place):
```bash
python skills/gopro-exif-injector/inject_gopro_exif.py "<PFAD>" --no-version
```
