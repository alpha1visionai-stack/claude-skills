---
name: gopro-exif-injector
description: >
  Injiziert realistische GoPro EXIF-Metadaten (HERO11/HERO12 Black, 2.7mm f/2.5 Linse, 15mm 35mm-Äquivalent), simuliert physikalische Kamera- & Sensor-Charakteristiken (Chromatische Aberration, S-Gradationskurve, RAW/CMOS-Sensorrauschen) und wendet DxO Nik 7 Color Efex Filter ("Ai-gen-2": Monday Morning Glow, Dual Film Grain, optional Darken/Lighten Center Vignette) an.
  Erzeugt automatisch versionierte Ausgabedateien (_v1, _v2, etc.) zum Schutz der Originale.
  Berücksichtigt automatisch oder manuell Tag- und Nachtszenen (ISO 100-3200, Verschlusszeit 1/30 bis 1/2000s, Program AE, GoPro Firmware).
  Verwenden, wenn der Benutzer sagt: "Füge GoPro EXIF Daten ein", "Schreibe realistische Metadaten in die Bilder", "GoPro Exif injecten", "Wende Nik 7 Color Efex Ai-gen-2 an", "Chromatische Aberration und Rauschen hinzufügen" oder ähnliches.
---

# GoPro EXIF, Sensor Realism & DxO Nik 7 Color Efex Skill

Dieses Tool kombiniert technisch akkurate GoPro EXIF-Metadaten mit physikalischer Sensor- und Optik-Simulation sowie dem **DxO Nik 7 Color Efex Preset `AI-gen-2`**, um KI-generierten Bildern die charakteristische Signatur echter Aufnahmen zu verleihen.

> 💾 **Auto-Versionierung:** Jeder Durchlauf erzeugt standardmäßig eine neue versionierte Datei (`dateiname_v1.jpg`, `dateiname_v2.jpg` etc.). Das Original bleibt unverändert.

---

## Enthaltene Bildverarbeitungs- & Filter-Pipeline

1. **DxO Nik 7 Color Efex `Ai-gen-2` Filterkette**:
   - **Monday Morning**: *Verschmieren auf 0* (volle Detailschärfe ohne künstliche Weichzeichnung/Diffusion), *Farbe erhöht* (+25% Farbsättigung für lebendige Farben) und feiner Helligkeitslift.
   - **Dual-Layer Film Grain**: Kombination aus weichem Korn und hochfrequentem Mikro-Korn mit Schatten- & Spitzlichterschutz.
   - **Darken / Lighten Center (optional, Standard: aus)**: Subtile Mitten-Aufhellung (+25%) bei fließender Rand-Vignettierung (kann via `--center-vignette` aktiviert und via `--vignette-strength <wert>` skaliert werden).
2. **Optische Sensor-Simulation**:
   - **Chromatische Aberration (Transversale CA / TCA)**: Radiale Farbverschiebungen (Rot outward / Blau inward), die zu den Bildrändern hin zunehmen (typisch für 15mm Superweitwinkel).
   - **Sensor-Gradationskurve (S-Curve)**: Schwarzwert-Lift (kein 0-Clipping) + weicher Highlight Roll-off (kein 255-Abriss).
   - **CMOS-Sensorrauschen**: Echtes, intensitätsgewichtetes Photonenrauschen in dunklen Bereichen.
3. **GoPro EXIF-Metadaten**:
   - Vollständiges EXIF-Profil (HERO12 Black / HERO11 Black, 2.7mm f/2.5, 15mm Äquivalent, ISO 100-3200, Program AE, Firmware v2.20).

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

- *"Wende DxO Nik 7 Color Efex mit dem Filter Ai-gen-2 auf die Bilder an."*
- *"Füge realistische GoPro EXIF-Daten, Sensor-Rauschen und Nik Color Efex Effekte ein."*
- *"Simuliere Chromatische Aberration, S-Kurve und das Ai-gen-2 Preset."*
- *"Wende den GoPro-Skill mit Center-Vignette an."*
- *"Öffne die Bilder in Nik 7 Color Efex."*

---

## CLI-Befehle

### 1. Standard (Erzeugt automatisch `_v1`, `_v2` etc.):
```bash
python skills/gopro-exif-injector/inject_gopro_exif.py "<PFAD_ZUM_ORDNER_ODER_BILD>"
```
*(Oder mit absolutem Pfad: `python "C:\Users\walte\.gemini\config\skills\gopro-exif-injector\inject_gopro_exif.py" "<PFAD>"`)*

### 2. Mit Center-Boost & Rand-Vignettierung (Darken/Lighten Center aktiviert):
```bash
python skills/gopro-exif-injector/inject_gopro_exif.py "<PFAD>" --center-vignette
```

### 3. Ohne Versionierung (Überschreibt Originaldatei direkt in-place):
```bash
python skills/gopro-exif-injector/inject_gopro_exif.py "<PFAD>" --no-version
```

### 4. Bilder in der DxO Nik 7 Color Efex Desktop-App öffnen:
```bash
python skills/gopro-exif-injector/inject_gopro_exif.py "<PFAD>" --open-nik
```

### 5. Nur EXIF ohne Filter/Effekte:
```bash
python skills/gopro-exif-injector/inject_gopro_exif.py "<PFAD>" --no-effects
```
