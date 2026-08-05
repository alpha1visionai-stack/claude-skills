---
name: luminar-preset-converter
description: >
  Durchsucht das aktuelle Projektverzeichnis oder einen angegebenen Ordner nach alten Luminar *.lmp Preset-Dateien sowie Adobe Lightroom *.xmp / *.lrtemplate Presets und konvertiert sie automatisch in das native Luminar Neo Format (.lnp Ordner mit lesbarem template.lmps JSON).
  Verwenden, wenn der Benutzer in natürlicher Sprache sagt: "Konvertiere meine Lightroom Presets für Luminar Neo", "Wandle lmp oder xmp Presets um", "Konvertiere alle Lightroom und Luminar Presets im Projektverzeichnis" oder ähnliches.
---

# Luminar Preset Converter Skill

Konvertiert legacy Luminar `*.lmp` Presets sowie **Adobe Lightroom `*.xmp` & `*.lrtemplate` Presets** direkt in das native Luminar Neo Format (`.lnp` Ordner mit `template.lmps` JSON-Dateien) im Root-Verzeichnis `Presets\Users\`.

## Unterstüzte Formate

- **Luminar Legacy (`.lmp`)**: Aus älteren Luminar-Versionen (Luminar 2018, 3, 4, Tonality).
- **Adobe Lightroom (`.xmp`)**: Standard-Voreinstellungen aus Lightroom Classic, Lightroom CC und Camera Raw.
- **Adobe Lightroom Legacy (`.lrtemplate`)**: Voreinstellungen aus älteren Lightroom-Versionen (Lightroom 4/5/6).

---

## Unterstützte Lightroom-Einstellungen (Mapping auf Luminar Neo)

- **Belichtung (`Exposure2012`)** $\rightarrow$ `MIPLExposureEffect`
- **Kontrast (`Contrast2012`)** $\rightarrow$ `MIPLContrastEffect`
- **Lichter (`Highlights2012`)** $\rightarrow$ `MIPLHighlightsEffect`
- **Tiefen (`Shadows2012`)** $\rightarrow$ `MIPLDynBrightnessEffect` (Smart Tone)
- **Weiß / Schwarz (`Whites2012`, `Blacks2012`)** $\rightarrow$ `MIPLBlackWhiteEffect`
- **Klarheit (`Clarity2012`)** $\rightarrow$ `MIPLClarityEffect`
- **Dunst entfernen (`Dehaze`)** $\rightarrow$ `MIPLDehazeEffect`
- **Dynamik & Sättigung (`Vibrance`, `Saturation`)** $\rightarrow$ `MIPLVibranceEffect` / `MIPLSaturationEffect`
- **Farbtemperatur & Tönung (`Temperature`, `Tint`)** $\rightarrow$ `MIPLDevelopCommonEffectID`
- **Schärfen (`Sharpness`)** $\rightarrow$ `MIPLSharpenEffect`
- **Vignettierung & Körnung (`PostCropVignetteAmount`, `GrainAmount`)** $\rightarrow$ `MIPLVignetteEffect` / `MIPLGrainNewEffect`

---

## Auslöser in natürlicher Sprache

- *"Konvertiere meine Lightroom Presets in Luminar Neo Presets."*
- *"Wandle alle xmp und lmp Dateien im Projektverzeichnis um."*
- *"Kannst du meine Lightroom .xmp Dateien für Luminar Neo konvertieren?"*

---

## Ausführungsanweisungen für den Agenten

```bash
python "C:\Users\walte\.gemini\config\skills\luminar-preset-converter\convert_lmp.py" "<PFAD_ZUM_ORDNER_ODER_PROJEKT>" [--out "<ZIEL_PFAD>"]
```
